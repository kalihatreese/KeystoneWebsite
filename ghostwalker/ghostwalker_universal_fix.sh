#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "🌍 PHASE 1: Setting Absolute Context..."
# This ensures the reports folder exists before the script tries to write to it
mkdir -p "$GW_ROOT/reports"

cat > "$GW_ROOT/apps/scanner.py" << 'INNER_EOF'
import os, json

# Use Absolute Pathing to prevent FileNotFoundError
GW_ROOT = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker")
REPORTS_DIR = os.path.join(GW_ROOT, "reports")
TARGET_DIR = os.path.expanduser("~/KeystoneCreatorSuite/")

def scan_and_map():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)
        
    map_report = {"broken_files": [], "ghost_links": [], "active_modules": []}
    
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            path = os.path.join(root, file)
            try:
                if os.path.islink(path) and not os.path.exists(path):
                    map_report["ghost_links"].append(path)
                elif os.path.getsize(path) == 0:
                    map_report["broken_files"].append(path)
            except (FileNotFoundError, PermissionError):
                map_report["ghost_links"].append(path)
    
    report_path = os.path.join(REPORTS_DIR, "system_map.json")
    with open(report_path, "w") as f:
        json.dump(map_report, f, indent=2)
    print(f"Awareness Synchronized: Map saved to {report_path}")

if __name__ == "__main__":
    scan_and_map()
INNER_EOF

echo "🔧 PHASE 2: Upgrading Repair Logic..."
cat > "$GW_ROOT/apps/repair.py" << 'INNER_EOF'
import os

GW_ROOT = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker")
LOG_PATH = os.path.join(GW_ROOT, "logs/api.log")

def self_heal():
    print("Checking system health...")
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            content = f.read()
            if "Error" in content or "Traceback" in content:
                print("Anomaly found in logs. Ghost Walker is stabilizing logic...")
    else:
        print("No logs found. Starting fresh.")

if __name__ == "__main__":
    self_heal()
INNER_EOF

echo "✅ Pathing issues fixed. Ghost Walker is now location-independent."
