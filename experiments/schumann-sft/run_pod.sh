#!/usr/bin/env bash
# Whole loop, unattended: up -> sync -> dry -> train+predict -> fetch -> down (this pod only).
set -uo pipefail
cd "$(dirname "$0")"
node runpod.mjs up || exit 1
S=$(cat ~/.ssh/runpod_schumann_pod.json)
IP=$(echo "$S" | python -c "import json,sys;print(json.load(sys.stdin)['publicIp'])")
PORT=$(echo "$S" | python -c "import json,sys;print(json.load(sys.stdin)['sshPort'])")
ID=$(echo "$S" | python -c "import json,sys;print(json.load(sys.stdin)['id'])")
SSH="ssh -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 -i $HOME/.ssh/runpod_rustline -p $PORT root@$IP"
node runpod.mjs sync || { node runpod.mjs down "$ID"; exit 1; }
$SSH "bash /workspace/schumann-sft/scripts/pod-bootstrap.sh dry" || { node runpod.mjs down "$ID"; exit 1; }
$SSH "cd /workspace/schumann-sft && SKIP_BASE=${SKIP_BASE:-} OUT=/workspace/schumann-sft/runs/${RUN_NAME:-seed13} bash scripts/pod-bootstrap.sh train > train.log 2>&1; tail -5 train.log"
node runpod.mjs fetch
node runpod.mjs down "$ID"
echo "RUN COMPLETE $(date)"
