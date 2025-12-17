#!/usr/bin/env bash
set -euo pipefail
echo "Sync helper: copy export files to Trinity models folder"
# edit the TRINITY_MODELS_DIR to where Trinity expects models
TRINITY_MODELS_DIR="${HOME}/Trinity/models"
SRC="$(pwd)/shadowx_export"
if [ ! -d "$SRC" ]; then
  echo "No export found at $SRC - please place Shadow X export there (weights + config)"
  exit 1
fi
mkdir -p "$TRINITY_MODELS_DIR"
cp -a "$SRC"/* "$TRINITY_MODELS_DIR"/
echo "Copied Shadow X export to $TRINITY_MODELS_DIR. Restart Trinity / ReeseOS services as needed."
