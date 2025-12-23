#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "📡 PHASE 1: Injecting Remote Notifier Module..."
cat > "$GW_ROOT/apps/notifier.py" << 'INNER_EOF'
import os
import requests
from datetime import datetime

# Place your Webhook URL here (Discord, Slack, etc.)
# If empty, it will just log locally to 'remote_history.log'
WEBHOOK_URL = os.getenv("GW_WEBHOOK", "")

def send_alert(message, alert_type="INFO"):
    payload = {
        "timestamp": datetime.now().isoformat(),
        "type": alert_type,
        "message": message,
        "admin": "ReeseDroid_Admin"
    }
    
    # Log locally
    log_path = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker/logs/remote_history.log")
    with open(log_path, "a") as f:
        f.write(f"[{alert_type}] {message}\n")
    
    # Try to send remotely
    if WEBHOOK_URL:
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
            print(f"🚀 Remote Alert Sent: {message}")
        except Exception as e:
            print(f"⚠️ Remote Alert Failed (Network?): {e}")
    else:
        print(f"📝 Local Alert Logged: {message}")

if __name__ == "__main__":
    send_alert("Ghost Walker Remote Listener is Online.", "SYSTEM_START")
INNER_EOF

echo "🔗 PHASE 2: Integrating Notifications into Core..."

# Injecting notification trigger into the Monetization engine
sed -i "/return {/i \    from .notifier import send_alert\n    send_alert(f'SALE CONFIRMED: {receipt_id} for ${amount}', 'REVENUE')" "$GW_ROOT/apps/monetization.py"

# Injecting notification trigger into the Repair engine
sed -i "/print(\"Anomaly detected/a \                from .notifier import send_alert\n                send_alert('System Anomaly Detected - Initiating Auto-Repair', 'CRITICAL')" "$GW_ROOT/apps/repair.py"

echo "✅ Remote Pulse is now integrated into Revenue and Repair loops."
