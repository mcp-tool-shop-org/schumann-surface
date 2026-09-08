#!/usr/bin/env bash
cd "$(dirname "$0")"
for spec in "NVIDIA RTX 6000 Ada Generation|SECURE" "NVIDIA L40S|SECURE" "NVIDIA A40|COMMUNITY" "NVIDIA RTX A6000|COMMUNITY"; do
  gpu="${spec%%|*}"; tier="${spec##*|}"; echo "== trying $gpu ($tier) $(date +%H:%M:%S)"
  RUNPOD_GPU="$gpu" RUNPOD_CLOUD_TYPE="$tier" bash run_ctx.sh && { echo "== SUCCESS on $gpu"; exit 0; }
done
echo "== ALL POOLS FAILED"
