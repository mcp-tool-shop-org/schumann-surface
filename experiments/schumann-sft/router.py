"""Deterministic router in front of the Schumann analyst.

Measured on the held-out set (runs/run2-30ep): the adapter alone is far better on per-month statistics
(0.944 vs 0.167 with context) because those numbers are not in the knowledge-base text; with the
knowledge base in context, a model is better on everything else. So:

    route(question) -> "adapter"  : the question names a specific month of the archive -> adapter, no context
                    -> "context"  : anything else -> model with the knowledge base in context

The month rule is the whole router. It is a regular expression, not a model, so it cannot drift and
its decisions are inspectable. `evaluate()` scores the routed system from saved predictions.
"""
import re

MONTHS = "january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec"
_YM = re.compile(r"\b(2013|2017)-(0[1-9]|1[0-2])\b")
_MONTH_YEAR = re.compile(rf"\b({MONTHS})\.?\s+(2013|2017)\b", re.I)
_YEAR_MONTH = re.compile(rf"\b(2013|2017)\s+({MONTHS})\b", re.I)
# Named-date facts that the knowledge base itself states (storm dates); those are KB facts, not statistics.
_KB_DATE = re.compile(r"\b(2013-10-02|2013-06-01)\b")


def route(question: str) -> str:
    q = question.strip()
    if _KB_DATE.search(q):
        return "context"
    if _YM.search(q) or _MONTH_YEAR.search(q) or _YEAR_MONTH.search(q):
        return "adapter"
    return "context"


def evaluate(pred_dir, context_condition="preds-base-context.jsonl", adapter_condition="preds-lora-epoch30.jsonl"):
    """Score the routed system by picking, per question, the saved answer of the routed condition."""
    import json, os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from grade import hit
    ctx = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(pred_dir, context_condition), encoding="utf-8"))}
    ada = {r["id"]: r for r in (json.loads(l) for l in open(os.path.join(pred_dir, adapter_condition), encoding="utf-8"))}
    per, routes = {}, {"adapter": 0, "context": 0}
    for qid, r in ctx.items():
        which = route(r["question"]); routes[which] += 1
        ans = (ada if which == "adapter" else ctx)[qid]["answer"]
        ok = all(hit(k, ans) for k in r["checks"])
        d = per.setdefault(r["kind"], [0, 0]); d[0] += ok; d[1] += 1
    tot = sum(v[0] for v in per.values()); n = sum(v[1] for v in per.values())
    return tot / n, {k: round(v[0] / v[1], 3) for k, v in per.items()}, routes


if __name__ == "__main__":
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else "runs/run2-30ep"
    for ctx_cond in ("preds-base-context.jsonl", "preds-lora-epoch30-context.jsonl"):
        acc, per, routes = evaluate(d, ctx_cond)
        print(f"routed with {ctx_cond:34s} all {acc:.3f}  {per}  routes {routes}")
