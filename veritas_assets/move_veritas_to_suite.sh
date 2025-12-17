#!/bin/bash
# Automated move for Veritas/ShadowX into KeystoneCreatorSuite
# Creates a dedicated folder and links dependencies

SUITE_DIR=~/KeystoneCreatorSuite
VERITAS_DIR=$SUITE_DIR/veritas_assets

mkdir -p "$VERITAS_DIR"

ASSETS=(
  ~/shadowx_installed
  ~/all_voices.json
  ~/veritas_speak.py
  ~/fetch_veritas.py
  ~/fetch_voices.py
  ~/reese_brain.json
  ~/veritas*.mp3
)

for asset in "${ASSETS[@]}"; do
  if [ -e "$asset" ]; then
    mv "$asset" "$VERITAS_DIR/"
    echo "Moved: $asset"
  else
    echo "Skipped (not found): $asset"
  fi
done

DEPENDENCIES=(
  ~/ghostwalker_snapshot_20251216_045421:ghostwalker_snapshot
  ~/mpt-7b-instruct:mpt_7b_model
  ~/Keystones-Trinity-Core:trinity_core
  ~/ReeseResonance:reese_resonance
)

cd "$VERITAS_DIR" || exit 1
for dep in "${DEPENDENCIES[@]}"; do
  SRC="${dep%%:*}"
  LINK_NAME="${dep##*:}"
  if [ -e "$SRC" ]; then
    ln -s "$SRC" "$LINK_NAME"
    echo "Linked: $LINK_NAME -> $SRC"
  else
    echo "Dependency missing, skipped: $SRC"
  fi
done

mkdir -p "$SUITE_DIR/keystone_output"
echo "All done. Veritas assets moved and dependencies linked."
