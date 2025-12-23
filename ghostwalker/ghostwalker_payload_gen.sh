#!/bin/bash
GW_ROOT="${HOME}/KeystoneCreatorSuite/ghostwalker"

echo "📦 PHASE 1: Injecting Payload Packager..."
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
    
    print(f"Packaging Ghost Walker into {zip_name}...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(GW_ROOT):
            # Skip the virtual environment and the zip itself
            if 'venv' in root or 'dist' in root or '__pycache__' in root:
                continue
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, GW_ROOT)
                zipf.write(file_path, arcname)
                
    print(f"✅ Payload Ready: {zip_path}")
    print(f"System is now ready for deployment/monetization.")

if __name__ == "__main__":
    create_payload()
INNER_EOF

echo "🚀 PHASE 2: Executing Final Packaging..."
python3 "$GW_ROOT/apps/packager.py"

echo "--- GHOST WALKER SUMMARY ---"
python3 "$GW_ROOT/apps/dashboard.py"
