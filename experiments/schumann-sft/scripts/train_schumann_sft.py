#!/usr/bin/env python3
"""Schumann SFT LoRA trainer — runs ON THE POD.

Inherits the paid-for parts of the studio's acoustic trainer: span-verified chat rendering with
the tokenizer's own template, prompt-loss weighting, chunked cross-entropy, pad collator, per-epoch
adapter checkpoints, and a receipt with hashes and package versions. No tool catalog here: the
examples are plain question/answer turns under one system prompt.

    python train_schumann_sft.py --data data/sft-train.jsonl --config lora-config.json --dry-run
    python train_schumann_sft.py --data data/sft-train.jsonl --config lora-config.json --out runs/seed13
"""
from __future__ import annotations
import argparse, hashlib, json, math, time
from pathlib import Path


def render_with_spans(tokenizer, messages):
    full = tokenizer.apply_chat_template(messages, tokenize=False)
    spans = []
    for i, m in enumerate(messages):
        if m["role"] != "assistant":
            continue
        before = tokenizer.apply_chat_template(messages[:i], tokenize=False, add_generation_prompt=True)
        after = tokenizer.apply_chat_template(messages[:i + 1], tokenize=False)
        if not after.startswith(before) or not full.startswith(after):
            raise AssertionError(f"template prefix property violated at turn {i}")
        spans.append((len(before), len(after)))
    return full, spans


def build_examples(lines, tokenizer, max_seq_len, plw, enforce):
    examples, lengths, over = [], [], []
    total = assist = 0
    for line in lines:
        text, spans = render_with_spans(tokenizer, line["messages"])
        enc = tokenizer(text, return_offsets_mapping=True, add_special_tokens=False)
        ids = enc["input_ids"]; lengths.append(len(ids))
        if len(ids) > max_seq_len:
            over.append({"id": line["id"], "tokens": len(ids)})
            if enforce:
                raise AssertionError(f"{line['id']} renders to {len(ids)} tokens > max_seq_len {max_seq_len}")
        w = [1.0 if any(s < e2 and s2 < e for s, e in spans) else plw for (s2, e2) in enc["offset_mapping"]]
        n = sum(1 for x in w if x == 1.0)
        if n == 0:
            raise AssertionError(f"{line['id']} produced no assistant tokens")
        total += len(ids); assist += n
        examples.append({"input_ids": ids, "labels": list(ids), "loss_weights": w})
    lengths.sort()
    return examples, {"examples": len(examples), "total_tokens": total, "assistant_tokens": assist,
                      "tokens_min": lengths[0], "tokens_median": lengths[len(lengths) // 2], "tokens_max": lengths[-1], "over": over}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--data", required=True)
    ap.add_argument("--out"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    lines = [json.loads(l) for l in Path(args.data).read_text(encoding="utf-8").splitlines() if l.strip()]
    if any(l.get("split") == "test" for l in lines):
        raise AssertionError("test rows leaked into the training file")
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(cfg["base_model"])
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    examples, st = build_examples(lines, tok, cfg["max_seq_len"], cfg.get("prompt_loss_weight", 0.1), enforce=not args.dry_run)
    print(f"[data] {st['examples']} examples | tokens min {st['tokens_min']} median {st['tokens_median']} max {st['tokens_max']} | total {st['total_tokens']} ({st['assistant_tokens']} assistant)")
    if args.dry_run:
        print(f"[dry-run] over max_seq_len: {len(st['over'])}; nothing downloaded beyond the tokenizer"); return
    if not args.out:
        raise SystemExit("--out required")

    import torch
    from torch.nn import CrossEntropyLoss
    from torch.utils.data import Dataset
    from transformers import AutoModelForCausalLM, Trainer, TrainerCallback, TrainingArguments, set_seed
    from peft import LoraConfig, get_peft_model

    class DS(Dataset):
        def __init__(self, items): self.items = items
        def __len__(self): return len(self.items)
        def __getitem__(self, i): return self.items[i]

    class Pad:
        def __init__(self, pid): self.pid = pid
        def __call__(self, batch):
            m = max(len(b["input_ids"]) for b in batch); ii, am, lb, ww = [], [], [], []
            for b in batch:
                n = len(b["input_ids"]); p = m - n
                ii.append(b["input_ids"] + [self.pid] * p); am.append([1] * n + [0] * p)
                lb.append(b["labels"] + [-100] * p); ww.append(b["loss_weights"] + [0.0] * p)
            return {"input_ids": torch.tensor(ii), "attention_mask": torch.tensor(am), "labels": torch.tensor(lb), "loss_weights": torch.tensor(ww, dtype=torch.float)}

    class WTrainer(Trainer):
        CH = 1024
        def compute_loss(self, model, inputs, return_outputs=False, **kw):
            weights = inputs.pop("loss_weights"); labels = inputs.pop("labels")
            out = model(**inputs); logits = out.logits
            sl, sw = labels[..., 1:], weights[..., 1:]; seq = logits.size(1) - 1; V = logits.size(-1)
            lf = CrossEntropyLoss(reduction="none", ignore_index=-100)
            tot = torch.zeros((), dtype=torch.float32, device=logits.device); ws = torch.zeros((), dtype=torch.float32, device=logits.device)
            for s in range(0, seq, self.CH):
                e = min(s + self.CH, seq); lg = logits[:, s:e, :].float(); lb = sl[:, s:e]; wt = sw[:, s:e]
                pt = lf(lg.reshape(-1, V), lb.reshape(-1)).reshape(lb.size()); w = wt * (lb != -100).float()
                tot = tot + (pt * w).sum(); ws = ws + w.sum()
            loss = tot / ws.clamp(min=1.0)
            return (loss, out) if return_outputs else loss

    class EpochCkpt(TrainerCallback):
        def __init__(self, out_dir, tok): self.out_dir, self.tok, self.saved = out_dir, tok, []
        def on_epoch_end(self, a, state, control, model=None, **kw):
            ep = int(round(state.epoch or 0))
            if ep and ep not in self.saved:
                p = self.out_dir / f"epoch{ep}"; model.save_pretrained(str(p)); self.tok.save_pretrained(str(p)); self.saved.append(ep); print(f"[checkpoint] {p}")

    out_dir = Path(args.out); out_dir.mkdir(parents=True, exist_ok=True); set_seed(cfg["seed"])
    try:
        model = AutoModelForCausalLM.from_pretrained(cfg["base_model"], dtype=torch.bfloat16, device_map="cuda")
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(cfg["base_model"], torch_dtype=torch.bfloat16, device_map="cuda")
    model.config.use_cache = False
    lc = cfg["lora"]
    model = get_peft_model(model, LoraConfig(r=lc["r"], lora_alpha=lc["alpha"], lora_dropout=lc["dropout"], bias="none", task_type="CAUSAL_LM", target_modules=list(lc["target_modules"])))
    model.enable_input_require_grads(); model.print_trainable_parameters()
    ta = TrainingArguments(output_dir=str(out_dir / "hf-out"), num_train_epochs=1 if args.smoke else cfg["epochs"], max_steps=1 if args.smoke else -1,
                           per_device_train_batch_size=cfg["per_device_train_batch_size"], gradient_accumulation_steps=cfg["gradient_accumulation_steps"],
                           learning_rate=cfg["lr"], lr_scheduler_type=cfg["schedule"], warmup_steps=cfg["warmup_steps"], weight_decay=cfg["weight_decay"],
                           max_grad_norm=cfg["max_grad_norm"], bf16=True, gradient_checkpointing=cfg["gradient_checkpointing"], gradient_checkpointing_kwargs={"use_reentrant": False},
                           logging_steps=1, save_strategy="no", report_to=[], seed=cfg["seed"], data_seed=cfg["seed"], remove_unused_columns=False)
    tr = WTrainer(model=model, args=ta, train_dataset=DS(examples), data_collator=Pad(tok.pad_token_id), callbacks=[EpochCkpt(out_dir, tok)])
    t0 = time.time(); res = tr.train(); dt = time.time() - t0
    import importlib.metadata as md
    receipt = {"base_model": cfg["base_model"], "config_sha256": hashlib.sha256(Path(args.config).read_bytes()).hexdigest(),
               "data_sha256": hashlib.sha256(Path(args.data).read_bytes()).hexdigest(), "data_stats": st, "train_seconds": round(dt, 1),
               "steps": res.global_step, "final_loss": res.training_loss, "log_history": tr.state.log_history,
               "versions": {p: (md.version(p) if p != "torch" else torch.__version__) for p in ("torch", "transformers", "peft", "accelerate")},
               "gpu": torch.cuda.get_device_name(0), "peak_mem_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2)}
    (out_dir / "training-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"[done] {res.global_step} steps in {dt/60:.1f} min, loss {res.training_loss:.4f}, peak {receipt['peak_mem_gb']} GB")


if __name__ == "__main__":
    main()
