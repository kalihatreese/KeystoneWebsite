#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "🛡️ PHASE 1: Upgrading Packager with Error-Handling..."
cat > "$GW_ROOT/apps/packager.py" << 'INNER_EOF'
import os
import zipfile
from datetime import datetime

GW_ROOT = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker")
DIST_DIR = os.path.join(GW_ROOT, "dist")

def create_payload():
    if not os.path.exists(DIST_DIR):
        os.makedirs(DIST_DIR)
        
    zip_name = f"GhostWalker_Payload_{datetime.now().strftime('%Y%m%d')}.zip"
    zip_path = os.path.join(DIST_DIR, zip_name)
    
    print(f"📦 Packaging Ghost Walker...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(GW_ROOT):
            if any(x in root for x in ['venv', 'dist', '__pycache__', '.git']):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                # FIX: Check if file actually exists and isn't a broken link
                if os.path.exists(file_path) and not os.path.islink(file_path):
                    arcname = os.path.relpath(file_path, GW_ROOT)
                    zipf.write(file_path, arcname)
                else:
                    print(f"⚠️ Skipping ghost file: {file}")
                
    print(f"✅ Secure Payload Ready: {zip_path}")

if __name__ == "__main__":
    create_payload()
INNER_EOF

echo "🔐 PHASE 2: Injecting Deployment Key Logic..."
cat > "$GW_ROOT/apps/lockdown.py" << 'INNER_EOF'
import hashlib

def generate_deployment_key(user_id):
    # Creates a unique key based on User ID + GhostWalker Salt
    salt = "GHOST_WALKER_2025_SECRET"
    key = hashlib.sha256(f"{user_id}{salt}".encode()).hexdigest()[:16].upper()
    print(f"--- DEPLOYMENT KEY GENERATED ---")
    print(f"User: {user_id}")
    print(f"Key: {key}")
    return key

if __name__ == "__main__":
    generate_deployment_key("ReeseDroid_Admin")
INNER_EOF

echo "🚀 PHASE 3: Final Execution..."
python3 "$GW_ROOT/apps/packager.py"
python3 "$GW_ROOT/apps/lockdown.py"
