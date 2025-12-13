#!/bin/bash
# setup_keystone_surplus_ai.sh - defensive launcher for Trinity services
set -euo pipefail
ROOT="\$HOME/KeystoneCreatorSuite"
TRINITY="\$ROOT/trinity"
LOG_DIR="\$ROOT/logs"
mkdir -p "\$LOG_DIR"

echo "=== Trinity SurplusAI / Trinity launcher ==="
# load .env into this shell if present (do not overwrite existing env vars)
if [ -f "\$TRINITY/.env" ]; then
  set -a
  # shellcheck disable=SC1090
  source "\$TRINITY/.env"
  set +a
  echo "🔐 Loaded \$TRINITY/.env"
else
  echo "⚠️  No .env at \$TRINITY/.env — process will run with current env"
fi

# ensure pm2 exists
if ! command -v pm2 >/dev/null 2>&1; then
  echo "❗ pm2 not installed. Install with: npm install -g pm2"
  exit 0
fi

# helper to start a service via pm2
start_pm2(){
  local path="\$1"; local name="\$2"
  if [ -f "\$path" ]; then
    echo "➡️  Starting \$name -> \$path"
    pm2 start "\$path" --name "\$name" --watch --output "\$LOG_DIR/\${name}.out.log" --error "\$LOG_DIR/\${name}.err.log" || pm2 restart "\$name"
  else
    echo "⚠️  Missing file for \$name: \$path"
  fi
}

# Try to locate likely service files anywhere under the repo (defensive)
echo "🔎 Locating service files..."
# explicit candidate locations (common)
declare -A CANDIDATES=(
  ["EmailWorker"]="\$ROOT/KeystoneSurplusAI/worker.js"
  ["EmailWorker2"]="\$ROOT/SurplusAI/worker.js"
  ["EmailWorker3"]="\$TRINITY/SurplusAI/worker.js"
  ["CyberCop"]="\$ROOT/CyberCop/main.js"
  ["TradingBot"]="\$ROOT/TradingBot/bot.js"
  ["Vault"]="\$ROOT/KEYSTONE_VAULT/server.js"
  ["Vault2"]="\$ROOT/KeystoneVault/server.js"
  ["Website"]="\$ROOT/keystone-storefront/server.js"
  ["Website2"]="\$ROOT/KeystoneWebsite/server.js"
  ["TrinityIndex"]="\$TRINITY/index.js"
)
# also search for any worker/main/server files elsewhere
mapfile -t FOUND < <(find "\$ROOT" -maxdepth 5 -type f \( -iname "worker.js" -o -iname "main.js" -o -iname "server.js" -o -iname "index.js" \) 2>/dev/null || true)
# add discovered files to candidates namespace with safe names
i=0
for f in "\${FOUND[@]:-}"; do
  # skip node_modules
  if echo "\$f" | grep -q "/node_modules/"; then continue; fi
  ((i++))
  CANDIDATES["Auto\${i}"]="\$f"
done

# Start each candidate that exists
echo "🔹 Starting discovered services (if present)..."
for key in "\${!CANDIDATES[@]}"; do
  # expand embedded vars safely
  eval path="\${CANDIDATES[\$key]}"
  # normalize name (remove slashes/spaces)
  name="\$key"
  # if the file exists, start
  if [ -f "\$path" ]; then
    start_pm2 "\$path" "\$name"
  fi
done

# Save pm2 state
pm2 save || true

# Print status and where logs are
echo ""
echo "=== PM2 LIST ==="
pm2 list

echo ""
echo "=== HEALTH CHECK & LOG SNIFF ==="
for svc in \$(pm2 jlist | jq -r '.[].name' 2>/dev/null || true); do
  echo "---- \$svc ----"
  pm2 describe "\$svc" || true
done

echo ""
echo "Logs are in: \$LOG_DIR"
echo "To follow a log: pm2 logs <name> --lines 200"
echo "To restart a service: pm2 restart <name>"
echo "To stop a service: pm2 stop <name>"
echo "If you need to add missing worker files, put them under \$ROOT and re-run this script."
echo "=== Done ==="
