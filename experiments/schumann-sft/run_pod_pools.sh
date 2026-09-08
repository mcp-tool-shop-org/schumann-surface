#!/usr/bin/env bash
# Try GPU pools in order; the first that deploys AND passes the dry-run gets the run.
cd "$(dirname "$0")"
for spec in "NVIDIA L40S|SECURE" "NVIDIA RTX 6000 Ada Generation|SECURE" "NVIDIA A40|COMMUNITY"; do
  gpu="${spec%%|*}"; tier="${spec##*|}"
  echo "== trying $gpu ($tier) $(date +%H:%M:%S)"
  RUNPOD_GPU="$gpu" RUNPOD_CLOUD_TYPE="$tier" bash run_pod.sh && { echo "== SUCCESS on $gpu"; exit 0; }
  echo "== $gpu did not complete; next pool"
done
echo "== ALL POOLS FAILED"
