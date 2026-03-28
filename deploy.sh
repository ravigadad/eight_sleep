#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$SCRIPT_DIR/.env" ]; then
  echo "Error: .env file not found. Copy .env.example to .env and fill in your values."
  exit 1
fi
source "$SCRIPT_DIR/.env"

# Validate required vars
for var in HA_SSH_USER HA_HOST; do
  if [ -z "${!var}" ]; then
    echo "Error: $var not set in .env"
    exit 1
  fi
done

HA_SSH="${HA_SSH_USER}@${HA_HOST}"
HA_DEST="/config/custom_components/eight_sleep/"

DRY_RUN=false

for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    *) echo "Unknown option: $arg"; exit 1 ;;
  esac
done

# Rsync only the integration code (never --delete, preserves __pycache__ etc on HA)
echo "Syncing custom_components/eight_sleep/ to $HA_SSH:$HA_DEST ..."
RSYNC_ARGS="-avz"
if $DRY_RUN; then
  RSYNC_ARGS="$RSYNC_ARGS --dry-run"
fi

rsync $RSYNC_ARGS \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude 'tests/' \
  "$SCRIPT_DIR/custom_components/eight_sleep/" "$HA_SSH:$HA_DEST"

if $DRY_RUN; then
  echo "Dry run complete — no changes made."
  exit 0
fi

echo "Restarting Home Assistant (required for Python changes)..."
ssh "$HA_SSH" 'ha core restart'
echo "Restart initiated. HA will be back in ~60s."
