#!/usr/bin/env python3
"""
Trinity Ledger Service — Immutable Ethical Record Layer
-------------------------------------------------------
Stores verified actions, decisions, and ethical outcomes from all Trinity nodes.
"""

import os, json, time, hashlib, datetime, threading, zmq

LEDGER_PATH = os.path.expanduser("~/Keystones-Trinity-Core/ledger.jsonl")
SIGN_KEY_PATH = os.path.expanduser("~/Ashleyana/.IMMORTAL_PAYLOAD")

def get_key():
    if not os.path.exists(SIGN_KEY_PATH):
        return "UNSIGNED"
    with open(SIGN_KEY_PATH) as f:
        return hashlib.sha256(f.read().encode()).hexdigest()[:32]

SIGN_KEY = get_key()

def sign_entry(data):
    payload = json.dumps(data, sort_keys=True)
    return hashlib.sha256((payload + SIGN_KEY).encode()).hexdigest()

def append_record(entry):
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def verify_entry(entry):
    sig = entry.get("signature")
    data = {k:v for k,v in entry.items() if k != "signature"}
    return sign_entry(data) == sig

def ledger_listener():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PULL)
    sock.bind("tcp://127.0.0.1:5577")
    print("[LEDGER] Service online — awaiting verified records.")
    while True:
        try:
            msg = sock.recv_json()
            msg["timestamp"] = datetime.datetime.now(datetime.UTC).isoformat()
            msg["signature"] = sign_entry(msg)
            append_record(msg)
            print(f"[LEDGER] Recorded: {msg.get('event','(unknown)')}")
        except Exception as e:
            print(f"[LEDGER] Error: {e}")
        time.sleep(0.1)

def verify_ledger():
    with open(LEDGER_PATH) as f:
        lines = [json.loads(line) for line in f]
    invalid = [e for e in lines if not verify_entry(e)]
    if invalid:
        print(f"[LEDGER] Integrity Warning: {len(invalid)} invalid entries detected.")
    else:
        print("[LEDGER] Integrity verified — all records valid.")

if __name__ == "__main__":
    threading.Thread(target=ledger_listener, daemon=True).start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[LEDGER] Shutting down.")
