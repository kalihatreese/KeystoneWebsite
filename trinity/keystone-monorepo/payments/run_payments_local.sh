#!/usr/bin/env bash
set -euo pipefail
BASE=~/KeystoneCreatorSuite/keystone-monorepo
cd "$BASE"
echo "[*] Start payments webhook (uvicorn) on port 9000"
nohup sh -c "uvicorn payments.webhook:app --host 0.0.0.0 --port 9000" > ~/KeystoneCreatorSuite/payments_webhook.log 2>&1 &
echo "[*] Logs: ~/KeystoneCreatorSuite/payments_webhook.log"
