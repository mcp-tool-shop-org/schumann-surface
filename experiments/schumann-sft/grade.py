"""Grade prediction files against the keys that travel with each test row. Runs on the studio rig, offline.

A row passes when every key hits: ("num", value, tol) = some number in the answer within tol;
("str", s) = substring, case-insensitive; ("any", [s1, s2, ...]) = at least one substring.
Numbers are extracted with a tolerant regex (commas, units and thousands separators stripped).

Usage: python experiments/schumann-sft/grade.py runs/seed13/preds-*.jsonl
"""
import glob, json, re, sys

NUM = re.compile(r"-?\d+(?:[.,]\d+)?")


def numbers(text):
    out = []
    for m in NUM.findall(text.replace(",", "")):
        try: out.append(float(m))
        except ValueError: pass
    return out


def hit(key, answer):
    kind = key[0]; low = answer.lower()
    if kind == "num":
        v, tol = float(key[1]), float(key[2])
        return any(abs(n - v) <= tol + 1e-9 for n in numbers(answer))
    if kind == "str":
        return key[1].lower() in low
    if kind == "any":
        return any(s.lower() in low for s in key[1])
    return False


def grade(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    per = {}
    for r in rows:
        ok = all(hit(k, r["answer"]) for k in r["checks"])
        d = per.setdefault(r["kind"], [0, 0]); d[0] += ok; d[1] += 1
    tot = sum(v[0] for v in per.values()); n = sum(v[1] for v in per.values())
    return tot / n if n else float("nan"), {k: (v[0] / v[1], v[1]) for k, v in per.items()}, n


if __name__ == "__main__":
    files = [f for a in sys.argv[1:] for f in glob.glob(a)]
    print(f"{'condition':34s} {'all':>7s}  {'paraphrase':>11s} {'unseen':>8s} {'data':>8s}")
    for f in sorted(files):
        acc, per, n = grade(f)
        cells = [f"{per[k][0]:.3f}" if k in per else "   -  " for k in ("paraphrase", "unseen", "data")]
        print(f"{f.split('/')[-1].split(chr(92))[-1]:34s} {acc:7.3f}  {cells[0]:>11s} {cells[1]:>8s} {cells[2]:>8s}   n={n}")
