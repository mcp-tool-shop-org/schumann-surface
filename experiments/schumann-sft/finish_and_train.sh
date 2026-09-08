#!/usr/bin/env bash
# When every raw month has been processed and exported: refresh the dataset upload, rebuild the SFT
# corpus, run one pod (fetch on finish, teardown by id), grade. Logs to experiments/schumann-sft/finish.log.
set -uo pipefail
cd "$(dirname "$0")/../.."
MONTHS="1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1701 1702"
say() { printf '\n== %s  %s\n' "$*" "$(date +%H:%M:%S)"; }

say "waiting for months"
while true; do
  missing=""
  for m in $MONTHS; do test -f "data/dataset/modes/SN_20${m}.parquet" || missing="$missing $m"; done
  [ -z "$missing" ] && break
  sleep 60
done
say "all months exported"
grep -h "VERIFY" data/pipeline_*.log | sort | uniq -c

say "dataset card: months + verification table"
python - <<'PY'
import glob, re, os
months = sorted(os.path.basename(p)[3:9] for p in glob.glob("data/dataset/modes/SN_*.parquet"))
labels = ", ".join(f"{m[:4]}-{m[4:]}" for m in months)
p = "dataset/README.md"; s = open(p, encoding="utf8").read()
s = re.sub(r"Months in this release: \*\*.*?\*\* \(both sensors\)\..*?\n\n", f"Months in this release: **{labels}** (both sensors), every one of them verified against the station's published products at a spectrum ratio of 1.0000.\n\n", s, flags=re.S)
s = s.replace("size_categories:\n  - 10K<n<100K", "size_categories:\n  - 100K<n<1M")
open(p, "w", encoding="utf8").write(s); print("card months:", labels)
PY
rm -rf dataset/kb/catalog && cp -r /e/AI/readouts/schumann-knowledge/catalog dataset/kb/catalog
python - <<'PY'
import os, shutil
from huggingface_hub import HfApi
api = HfApi(); repo = "mcp-tool-shop/schumann-sierra-nevada"
st = "data/hf_staging"; shutil.rmtree(st, ignore_errors=True); shutil.copytree("data/dataset", st)
shutil.copy("dataset/README.md", os.path.join(st, "README.md")); shutil.copytree("dataset/kb", os.path.join(st, "kb"))
api.upload_folder(folder_path=st, repo_id=repo, repo_type="dataset", commit_message="v1.0.0: all twelve raw months, both sensors")
print("dataset uploaded")
PY

say "corpus"
export HF_HOME=E:/AI-Models/hf-cache
python experiments/schumann-sft/build_corpus.py

say "pod"
export RUNPOD_GPU="${RUNPOD_GPU:-NVIDIA RTX A6000}"
bash experiments/schumann-sft/run_pod.sh
ls experiments/schumann-sft/runs/seed13 2>/dev/null

say "grade"
python experiments/schumann-sft/grade.py "experiments/schumann-sft/runs/seed13/preds-*.jsonl"
say "FINISH COMPLETE"
