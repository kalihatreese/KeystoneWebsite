#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "🔧 REPAIRING: Updating Scanner to handle broken directories..."
cat > "$GW_ROOT/apps/scanner.py" << 'INNER_EOF'
import os, json

def scan_and_map():
    target = os.path.expanduser("~/KeystoneCreatorSuite/")
    map_report = {"broken_files": [], "ghost_links": [], "active_modules": []}
    
    for root, dirs, files in os.walk(target):
        for file in files:
            path = os.path.join(root, file)
            try:
                if os.path.islink(path) and not os.path.exists(path):
                    map_report["ghost_links"].append(path)
                elif os.path.getsize(path) == 0:
                    map_report["broken_files"].append(path)
            except FileNotFoundError:
                map_report["ghost_links"].append(path)
    
    with open("../reports/system_map.json", "w") as f:
        json.dump(map_report, f, indent=2)
    print(f"Awareness Updated: {len(map_report['ghost_links'])} dead links ignored.")

if __name__ == "__main__":
    scan_and_map()
INNER_EOF

echo "💰 MONITORING: Injecting Revenue Dashboard..."
cat > "$GW_ROOT/apps/dashboard.py" << 'INNER_EOF'
import os

def show_revenue():
    log_path = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker/logs/payments.log")
    if not os.path.exists(log_path):
        print("Revenue: $0.00 (No sales logged yet)")
        return
    
    with open(log_path, "r") as f:
        lines = f.readlines()
        total = sum(float(line.split("|")[2].replace("$", "")) for line in lines)
        print(f"--- GHOST WALKER REVENUE ---")
        print(f"Total Sales: {len(lines)}")
        print(f"Total Revenue: ${total:.2f}")
        print(f"System Status: AUTONOMOUS")

if __name__ == "__main__":
    show_revenue()
INNER_EOF

echo "✅ Ghost Walker is now aware of the broken links and the Revenue Dash is ready."
