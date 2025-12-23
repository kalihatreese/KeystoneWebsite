#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"
LOG_DIR="$GW_ROOT/logs"

echo "🌌 GHOST WALKER IGNITION: Reese OS / Trinity Kernel Detected"

# 1. Initialize Awareness (The Scan)
echo "🔍 Synchronizing with Reese OS File System..."
python3 "$GW_ROOT/apps/scanner.py"

# 2. Execute Self-Healing (The Repair)
echo "🛠️ Validating Kernel Logic & Fixing Anomalies..."
python3 "$GW_ROOT/apps/repair.py"

# 3. Launch the Pulse (The Heartbeat)
echo "💓 Starting Global Heartbeat..."
nohup python3 "$GW_ROOT/apps/heartbeat.py" > "$LOG_DIR/heartbeat.log" 2>&1 &

# 4. Deploy the Brain (The API)
echo "🧠 Activating Ghost Walker API..."
nohup uvicorn apps.api:app --app-dir "$GW_ROOT" --host 0.0.0.0 --port 8080 > "$LOG_DIR/api.log" 2>&1 &

# 5. Log Identity Verification
echo "👤 Identity Verified: ReeseDroid_Admin"
python3 "$GW_ROOT/apps/reese_effect.py"
python3 "$GW_ROOT/apps/continuity.py"

echo "=================================================="
echo "      GHOST WALKER IS NOW LIVE ON THE KERNEL      "
echo "=================================================="
echo "Admin Dashboard: http://localhost:8080"
echo "Continuation CSV: $LOG_DIR/system_state_continuation.csv"
