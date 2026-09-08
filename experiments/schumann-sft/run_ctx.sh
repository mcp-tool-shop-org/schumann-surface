#!/usr/bin/env bash
# Prediction-only pod: adapter + KB in context. up -> sync -> scp adapter -> ctx -> fetch -> down by id.
set -uo pipefail
cd "$(dirname "$0")"
sed -i 's/$//' scripts/*.sh scripts/*.py lora-config.json
ADAPTER="${1:-runs/run2-30ep/epoch30}"
node runpod.mjs up || exit 1
S=$(cat ~/.ssh/runpod_schumann_pod.json)
IP=$(echo "$S" | python -c "import json,sys;print(json.load(sys.stdin)['publicIp'])")
PORT=$(echo "$S" | python -c "import json,sys;print(json.load(sys.stdin)['sshPort'])")
ID=$(echo "$S" | python -c "import json,sys;print(json.load(sys.stdin)['id'])")
K="$HOME/.ssh/runpod_rustline"; O="-o StrictHostKeyChecking=accept-new -o ConnectTimeout=20"
node runpod.mjs sync || { node runpod.mjs down "$ID"; exit 1; }
scp -r -P "$PORT" -i "$K" $O "$ADAPTER" "root@$IP:/workspace/schumann-sft/adapter" || { node runpod.mjs down "$ID"; exit 1; }
ssh -i "$K" -p "$PORT" $O "root@$IP" "cd /workspace/schumann-sft && pip install --quiet --no-input --break-system-packages 'transformers>=4.44' 'peft>=0.13' 'accelerate>=0.34' && OUT=/workspace/schumann-sft/runs/ctx bash scripts/pod-bootstrap.sh ctx > ctx.log 2>&1; tail -4 ctx.log"
mkdir -p runs && scp -r -P "$PORT" -i "$K" $O "root@$IP:/workspace/schumann-sft/runs/ctx" runs/
node runpod.mjs down "$ID"
echo "CTX COMPLETE $(date)"
