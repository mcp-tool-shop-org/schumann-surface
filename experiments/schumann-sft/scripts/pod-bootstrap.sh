#!/usr/bin/env bash
# Schumann SFT — what runs ON THE POD, in order, once files are synced.
# Ordered by cost: GPU, deps, data dry-run (no weights), then train, then predict.
#   bash pod-bootstrap.sh dry
#   bash pod-bootstrap.sh train      # train + the three prediction conditions
# It never tears the pod down; that is done from the studio rig (node runpod.mjs down).
set -euo pipefail
MODE="${1:-dry}"
WORK="${WORK:-/workspace/schumann-sft}"
OUT="${OUT:-$WORK/runs/seed13}"
say() { printf '\n\033[1m== %s\033[0m\n' "$*"; }

say "GPU"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
python3 - <<'PY'
import torch, sys
if not torch.cuda.is_available(): sys.exit("FATAL: torch cannot see the GPU.")
cap = torch.cuda.get_device_capability(0); print(f"torch {torch.__version__} | cuda {torch.version.cuda} | sm_{cap[0]}{cap[1]}")
PY

say "Dependencies"
pip install --quiet --no-input --break-system-packages "transformers>=4.44" "peft>=0.13" "accelerate>=0.34"
python3 -c "import importlib.metadata as md; print({p: md.version(p) for p in ('torch','transformers','peft','accelerate')})"

say "Data present"
for f in data/sft-train.jsonl data/sft-test.jsonl data/kb-context.md lora-config.json; do test -f "$WORK/$f" || { echo "FATAL: missing $f"; exit 1; }; done
wc -l "$WORK/data/sft-train.jsonl" "$WORK/data/sft-test.jsonl"

case "$MODE" in
  dry)
    python3 "$WORK/scripts/train_schumann_sft.py" --data "$WORK/data/sft-train.jsonl" --config "$WORK/lora-config.json" --dry-run
    ;;
  train)
    say "Training"
    python3 "$WORK/scripts/train_schumann_sft.py" --data "$WORK/data/sft-train.jsonl" --config "$WORK/lora-config.json" --out "$OUT"
    say "Predictions: base (fair), base + KB context, adapter (no context)"
    P="$WORK/scripts/predict_schumann.py"; T="$WORK/data/sft-test.jsonl"; C="$WORK/lora-config.json"
    if [ -z "${SKIP_BASE:-}" ]; then
      python3 "$P" --config "$C" --data "$T" --out "$OUT/preds-base-fair.jsonl"
      python3 "$P" --config "$C" --data "$T" --context "$WORK/data/kb-context.md" --out "$OUT/preds-base-context.jsonl"
    fi
    for e in $(ls -d "$OUT"/epoch* | xargs -n1 basename); do
      python3 "$P" --config "$C" --data "$T" --adapter "$OUT/$e" --out "$OUT/preds-lora-$e.jsonl"
    done
    say "Done — pull $OUT to the studio rig, then: node runpod.mjs down --all"
    ;;
  ctx)
    say "Adapter + KB context (the fourth condition); adapter synced to $WORK/adapter"
    test -d "$WORK/adapter" || { echo "FATAL: no adapter at $WORK/adapter"; exit 1; }
    mkdir -p "$OUT"
    python3 "$WORK/scripts/predict_schumann.py" --config "$WORK/lora-config.json" --data "$WORK/data/sft-test.jsonl" --adapter "$WORK/adapter" --context "$WORK/data/kb-context.md" --out "$OUT/preds-lora-context.jsonl"
    say "Done — pull $OUT, then tear down by id"
    ;;
  *) echo "usage: bash pod-bootstrap.sh [dry|train|ctx]"; exit 2 ;;
esac
say "The pod is STILL BILLING"
