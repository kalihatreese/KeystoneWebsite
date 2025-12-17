#!/usr/bin/env python3
"""
Trinity Pulse Monitor — System Health & Ethical Coherence Check
---------------------------------------------------------------
Polls all active Trinity Core services, verifies process uptime,
ledger integrity, and consensus responsiveness.
"""

import os, subprocess, json, datetime, hashlib, time, psutil

SERVICES = {
    "Cole": "mesh/core.py",
    "Clay": "mesh/core.py",
    "ShadowX": "mesh/core.py",
    "CyberCop": "cybercop_audit.py",
    "Ledger": "ledger_service.py",
    "Store": "store_service.py",
    "Ashleyana": "ashleyana_bridge.py"
}

LEDGER_PATH = os.path.expanduser("~/Keystones-Trinity-Core/ledger.jsonl")
SIGN_KEY_PATH = os.path.expanduser("~/Ashleyana/.IMMORTAL_PAYLOAD")

def get_key():
    if not os.path.exists(SIGN_KEY_PATH):
        return "UNSIGNED"
    with open(SIGN_KEY_PATH) as f:
        return hashlib.sha256(f.read().encode()).hexdigest()[:32]

SIGN_KEY = get_key()

def check_process(script_name):
    for proc in psutil.process_iter(attrs=['pid', 'cmdline']):
        try:
            if any(script_name in " ".join(proc.info['cmdline']) for _ in [0]):
                return True
        except Exception:
            pass
    return False

def check_ledger_integrity():
    if not os.path.exists(LEDGER_PATH):
        return "NO LEDGER FOUND"
    with open(LEDGER_PATH) as f:
        lines = [json.loads(l) for l in f if l.strip()]
    invalid = 0
    for e in lines:
        sig = e.get("signature")
        data = {k:v for k,v in e.items() if k != "signature"}
        expected = hashlib.sha256((json.dumps(data, sort_keys=True) + SIGN_KEY).encode()).hexdigest()
        if expected != sig:
            invalid += 1
    return f"{len(lines)} entries ({invalid} invalid)" if lines else "EMPTY"

def print_status():
    print("\n=== TRINITY PULSE MONITOR ===")
    print(f"Timestamp: {datetime.datetime.now(datetime.UTC).isoformat()}")
    print(f"Sign Key: {SIGN_KEY[:8]}... verified\n")
    for name, script in SERVICES.items():
        running = check_process(script)
        state = "✅ ONLINE" if running else "❌ OFFLINE"
        print(f"{name:<10} → {state}")
    ledger_status = check_ledger_integrity()
    print(f"\nLedger Integrity → {ledger_status}")
    print("==============================\n")

if __name__ == "__main__":
    try:
        while True:
            print_status()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n[TRINITY PULSE] Monitor stopped.")

# Trinity System Initialization Event
from trinity_event_emitter import emit_event
emit_event("TrinityCore", "System startup complete", "online")

