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
