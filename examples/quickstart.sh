#!/bin/sh
# Quickstart: exercise every tool once, in a scratch directory.
# Nothing outside the scratch directory is touched.
set -eu
cd "$(dirname "$0")/.."
SCRATCH="$(mktemp -d)"
trap 'rm -rf "$SCRATCH"' EXIT

echo "== work registry =="
python3 tools/work_registry.py --file "$SCRATCH/registry.json" add "write the summary" --lane docs
python3 tools/work_registry.py --file "$SCRATCH/registry.json" add "backfill the index" --lane maintenance
python3 tools/work_registry.py --file "$SCRATCH/registry.json" claim 1 --owner worker-a
python3 tools/work_registry.py --file "$SCRATCH/registry.json" close 1 --evidence "summary drafted and verified"
python3 tools/work_registry.py --file "$SCRATCH/registry.json" list
python3 tools/work_registry.py --file "$SCRATCH/registry.json" next

echo "== lease =="
python3 tools/lease.py --file "$SCRATCH/leases.json" acquire workstation --holder worker-a --ttl 600
python3 tools/lease.py --file "$SCRATCH/leases.json" status
python3 tools/lease.py --file "$SCRATCH/leases.json" release workstation --holder worker-a

echo "== liveness (this shell as the 'job') =="
echo $$ > "$SCRATCH/job.pid"
touch "$SCRATCH/job.log"
python3 tools/liveness.py --pid-file "$SCRATCH/job.pid" --output-file "$SCRATCH/job.log" --max-age 300

echo "== grading =="
python3 tools/grade.py examples/findings.example.json || true

echo "quickstart OK"
