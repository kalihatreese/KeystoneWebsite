"""
core/trinity_loader.py
Index & register Trinity modules safely without executing them.
"""
import os
import json

TRINITY_INDEX = "core/trinity_index.json"
TRINITY_DIRS = ["core/trinity_modules", "trinity", "Trinity"]

def index_trinity_modules():
    modules = []
    for base in TRINITY_DIRS:
        if not os.path.exists(base):
            continue
        for root, dirs, files in os.walk(base):
            for f in files:
                if f.endswith(".py") and f != "__init__.py":
                    path = os.path.join(root, f)
                    modules.append({
                        "name": os.path.splitext(f)[0],
                        "path": path,
                        "root": root
                    })
    with open(TRINITY_INDEX, "w", encoding="utf-8") as fh:
        json.dump(modules, fh, indent=2)
    return modules

def load_index():
    if os.path.exists(TRINITY_INDEX):
        import json
        with open(TRINITY_INDEX, "r", encoding="utf-8") as fh:
            return json.load(fh)
    return []
