#!/data/data/com.termux/files/usr/bin/bash
# === Keystone Autotrend Vault Auto-Startup ===
cd ~/Autotrend_vault || exit

# activate Python venv if present
[ -f .venv/bin/activate ] && source .venv/bin/activate

# optional: silent git pull
git pull --ff-only >/dev/null 2>&1 || true

# build the store if script exists
if [ -f scripts/build_store.py ]; then
  python scripts/build_store.py >/dev/null 2>&1 &
fi

# serve static site (port 3100)
nohup python3 -m http.server 3100 --directory docs >/dev/null 2>&1 &

# log event
echo "[BOOT] $(date '+%Y-%m-%d %H:%M:%S') Autotrend Vault started" >> ~/autotrend_boot.log
