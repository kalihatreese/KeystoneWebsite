import os
import sys

# Absolute pathing for Reese OS / Trinity environment
GW_ROOT = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker")
sys.path.append(os.path.join(GW_ROOT, "apps"))

# Import standalone notifier
import notifier

LOG_PATH = os.path.join(GW_ROOT, "logs/api.log")

def self_heal():
    print("🛠️ Ghost Walker: Validating Kernel Logic...")
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            content = f.read()
            if "Error" in content or "Traceback" in content:
                # SEND REMOTE PULSE
                notifier.send_alert("⚠️ System Anomaly Detected - Initiating Auto-Repair", "CRITICAL")
                print("Anomaly detected. Ghost Walker is stabilizing logic...")
    else:
        print("✅ System Healthy: No logs to repair.")

if __name__ == "__main__":
    self_heal()
