import time, hmac, hashlib, os, json, pathlib

STORE=os.path.expanduser("~/KeystoneCreatorSuite/keystone-payments")
pathlib.Path(STORE).mkdir(parents=True, exist_ok=True)
DB_FILE = os.path.join(STORE, "licenses.json")

def _load():
    try:
        with open(DB_FILE,"r") as fh:
            return json.load(fh)
    except:
        return []

def _save(data):
    with open(DB_FILE,"w") as fh:
        json.dump(data, fh, indent=2)

def create_license_for_session(session_id: str, sku: str=""):
    key_raw = f"{session_id}-{int(time.time())}"
    secret = os.getenv("STRIPE_SECRET_KEY","reese-default-secret")
    sig = hmac.new(secret.encode(), key_raw.encode(), hashlib.sha256).hexdigest()[:20]
    license_key = f"{key_raw}-{sig}"
    rec = {"session": session_id, "sku": sku, "license": license_key, "when": int(time.time())}
    data = _load()
    data.append(rec)
    _save(data)
    return license_key

def list_licenses():
    return _load()
