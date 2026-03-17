#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="${ROOT}/tmp"
mkdir -p "$TMP_DIR"

cat > "$TMP_DIR/rare_process.spl" <<'SPL'
index=win EventCode=1
| stats dc(host) as hosts by process_name
| where hosts=1
SPL

python3 "$ROOT/scripts/translate_workflow.py" translate \
  --title "rare process execution" \
  --spl-file "$TMP_DIR/rare_process.spl" \
  --source "CrowdStrike LogScale / Endpoint telemetry" \
  --goal "Detect processes executed on a single host" \
  --fields "host,process_name,FileName,aid"

echo "Done. Check the runs/ directory."
