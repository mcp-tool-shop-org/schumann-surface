---
license: apache-2.0
base_model: Qwen/Qwen2.5-3B-Instruct
library_name: peft
tags:
  - lora
  - schumann-resonance
  - geophysics
  - knowledge-injection
datasets:
  - mcp-tool-shop/schumann-sierra-nevada
language:
  - en
---

# schumann-analyst · Qwen2.5-3B LoRA

A small adapter that knows one dataset: [mcp-tool-shop/schumann-sierra-nevada](https://huggingface.co/datasets/mcp-tool-shop/schumann-sierra-nevada),
calibrated Schumann resonance products from the Sierra Nevada ELF station. It answers questions about
the station, its calibration, the processing chain, the licences, the event lanes, and the per-month
statistics without the documents in context.

This is a knowledge-injection experiment, reported with the controls that make the number mean
something. The base model fairly prompted, and the base model with the knowledge base pasted into the
prompt, sit beside the adapter on the same held-out questions.

## Results

__RESULTS_TABLE__

Test questions (n = __N_TEST__): **paraphrase** = a held-out phrasing of a fact the adapter trained on;
**unseen** = a fact never rendered as a training pair; **data** = a per-month statistic computed from
the Parquet tables. Grading is key-based (numbers within tolerance, required substrings), offline, from
saved raw completions.

How to read it: the gap between "base + KB in context" and "adapter, no context" is the honest
measure of what the adapter internalised versus what retrieval would have supplied. The "unseen"
column bounds what it can do beyond memorising the corpus.

## Training

- Base: Qwen/Qwen2.5-3B-Instruct, bf16. LoRA r = 16, α = 32, dropout 0.05, on q/k/v/o and gate/up/down.
- Corpus: __N_TRAIN__ question/answer pairs under one system prompt (__TOKENS__ tokens per epoch),
  built from the dataset's `kb/` documents and from statistics computed over all twelve months.
- 4 epochs, lr 2e-4 cosine, effective batch 16, prompt-loss weight 0.1, seed 13.
- __GPU__, __TRAIN_MIN__ minutes of training, peak __PEAK_GB__ GB. Receipt: `training-receipt.json`.


## The router (use this, not the bare adapter)

`router.py` in the repository is a regular expression, not a model: a question that names a specific
month of the archive goes to the adapter alone; everything else goes to the adapter with the
knowledge base in context. Scored from the saved held-out answers:

| System | all | paraphrase | unseen | data |
|---|---|---|---|---|
| best single condition (adapter alone) | 0.573 | 0.425 | 0.200 | 0.944 |
| **routed: month → adapter, else → adapter + KB context** | **0.625** | 0.525 | 0.250 | 0.944 |
| routed: month → adapter, else → base + KB context | 0.594 | 0.375 | 0.400 | 0.944 |

`analyst.py` wraps the model with the router in front and returns every answer with its route and
the model that produced it. `--else base` picks the second row's variant, which is worse overall but
better on facts the corpus never contained.

## Use

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
base = "Qwen/Qwen2.5-3B-Instruct"
tok = AutoTokenizer.from_pretrained(base)
model = PeftModel.from_pretrained(AutoModelForCausalLM.from_pretrained(base, torch_dtype="bfloat16", device_map="cuda"), "mcp-tool-shop/schumann-analyst-qwen2.5-3b-lora")
msgs = [{"role": "system", "content": "You are the analyst for the schumann-sierra-nevada dataset: calibrated Schumann resonance products derived from the Sierra Nevada ELF station's open raw archive. Answer precisely, give numbers and units when you know them, and say plainly when something is a model rather than a measurement."},
        {"role": "user", "content": "Why does the data stop at 25 Hz?"}]
ids = tok.apply_chat_template(msgs, add_generation_prompt=True, return_tensors="pt").to("cuda")
print(tok.decode(model.generate(ids, max_new_tokens=160)[0][ids.shape[1]:], skip_special_tokens=True))
```

## Limits

It knows this dataset and this station. It does not know other stations, other years, or physics
beyond what the knowledge base states. Numbers it gives should be checked against the dataset tables
for anything that matters; the adapter is a convenience, the Parquet is the record.

## Provenance

Code and corpus builder: [mcp-tool-shop-org/schumann-surface](https://github.com/mcp-tool-shop-org/schumann-surface)
(`experiments/schumann-sft/`). Data: Salinas et al., Zenodo 10.5281/zenodo.6348930 (CC BY 4.0), via the
dataset above. Adapter weights Apache-2.0, following the base model's licence.
