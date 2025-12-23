#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"
source "${GW_ROOT}/venv/bin/activate"
echo "Ghost Walker Prime is now controlling the environment."
python3 apps/scanner.py
python3 apps/repair.py
nohup uvicorn apps.api:app --host 0.0.0.0 --port 8080 > "${GW_ROOT}/logs/api.log" 2>&1 &
echo "Full Autonomy Active. Monitor via ~/KeystoneCreatorSuite/ghostwalker/reports/"
