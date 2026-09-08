#!/usr/bin/env python3
"""Generate answers on the held-out questions: base model (fair prompt), base + KB in context, or adapter.

Writes one JSONL line per test question: {"id", "kind", "question", "gold", "answer"}. The raw
completion is always saved; grading happens on the studio rig from the saved text so a grader bug can
be fixed without a GPU (the acoustic run's lesson).

    python predict_schumann.py --config lora-config.json --data data/sft-test.jsonl --out preds-base-fair.jsonl
    python predict_schumann.py ... --context data/kb-context.md --out preds-base-context.jsonl
    python predict_schumann.py ... --adapter runs/seed13/epoch4 --out preds-lora-epoch4.jsonl
"""
from __future__ import annotations
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True); ap.add_argument("--data", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--adapter"); ap.add_argument("--context", help="markdown file to prepend as reference material (the RAG control)")
    ap.add_argument("--max-new-tokens", type=int, default=160)
    args = ap.parse_args()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    cfg = json.loads(Path(args.config).read_text(encoding="utf-8"))
    tok = AutoTokenizer.from_pretrained(cfg["base_model"]); tok.padding_side = "left"
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    try:
        model = AutoModelForCausalLM.from_pretrained(cfg["base_model"], dtype=torch.bfloat16, device_map="cuda")
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(cfg["base_model"], torch_dtype=torch.bfloat16, device_map="cuda")
    which = "base"
    if args.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter); which = args.adapter
    model.eval()
    context = Path(args.context).read_text(encoding="utf-8") if args.context else None
    lines = [json.loads(l) for l in Path(args.data).read_text(encoding="utf-8").splitlines() if l.strip()]
    print(f"[predict] {which} | {len(lines)} questions | context={'yes' if context else 'no'}")
    out = open(args.out, "w", encoding="utf-8")
    B = 8
    for i in range(0, len(lines), B):
        batch = lines[i:i + B]; prompts = []
        for line in batch:
            msgs = [m for m in line["messages"] if m["role"] != "assistant"]
            if context:
                msgs = [msgs[0], {"role": "user", "content": "Reference material:\n\n" + context + "\n\nAnswer the question using the reference material. Be concise and give numbers where the material has them.\n\nQuestion: " + msgs[1]["content"]}]
            prompts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True))
        enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
        with torch.no_grad():
            gen = model.generate(**enc, max_new_tokens=args.max_new_tokens, do_sample=False, pad_token_id=tok.pad_token_id)
        for line, g in zip(batch, gen):
            text = tok.decode(g[enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()
            gold = next(m["content"] for m in line["messages"] if m["role"] == "assistant")
            out.write(json.dumps({"id": line["id"], "kind": line.get("kind"), "question": line["messages"][1]["content"], "gold": gold, "answer": text, "checks": line.get("checks")}, ensure_ascii=False) + "\n")
        print(f"[predict] {min(i + B, len(lines))}/{len(lines)}", flush=True)
    out.close(); print(f"[predict] wrote {args.out}")


if __name__ == "__main__":
    main()
