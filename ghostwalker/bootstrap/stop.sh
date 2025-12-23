#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "🏁 Initiating Graceful Shutdown..."

# 1. Trigger the Continuation Logic one last time
python3 "$GW_ROOT/apps/continuity.py"

# 2. Halt Services
echo "Stopping Ghostwalker services (Uvicorn & Heartbeat)..."
pkill -f "uvicorn" || true
pkill -f "heartbeat.py" || true

echo "💾 State saved. System Halted."
