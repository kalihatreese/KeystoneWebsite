#!/usr/bin/env python3
"""
core/approve.py
Simple CLI to list, approve, or deny queued actions in core/approval_queue.json.
Approvals are written to core/approval_approved.json or core/approval_denied.json.
"""

import json
import os
import sys
from datetime import datetime

APPROVAL_FILE = "core/approval_queue.json"
APPROVED_FILE = "core/approval_approved.json"
DENIED_FILE = "core/approval_denied.json"

def load_queue():
    if not os.path.exists(APPROVAL_FILE):
        return []
    with open(APPROVAL_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_queue(q):
    with open(APPROVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)

def append_record(fname, record):
    arr = []
    if os.path.exists(fname):
        try:
            with open(fname, "r", encoding="utf-8") as f:
                arr = json.load(f)
        except Exception:
            arr = []
    arr.append(record)
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(arr, f, indent=2)

def list_queue():
    q = load_queue()
    if not q:
        print("Approval queue is empty.")
        return
    for i, item in enumerate(q):
        print(f"[{i}] id={item.get('id','<no-id>')} kind={item.get('kind','')} risk={item.get('risk','')} desc={item.get('description','')[:120]}")

def approve(index):
    q = load_queue()
    try:
        item = q.pop(index)
    except IndexError:
        print("Invalid index.")
        return
    item['_approved_at'] = datetime.utcnow().isoformat() + "Z"
    append_record(APPROVED_FILE, item)
    save_queue(q)
    print(f"Approved item at index {index} (id={item.get('id')}).")

def deny(index):
    q = load_queue()
    try:
        item = q.pop(index)
    except IndexError:
        print("Invalid index.")
        return
    item['_denied_at'] = datetime.utcnow().isoformat() + "Z"
    append_record(DENIED_FILE, item)
    save_queue(q)
    print(f"Denied item at index {index} (id={item.get('id')}).")

def help_text():
    print("Usage: approve.py list")
    print("       approve.py approve <index>")
    print("       approve.py deny <index>")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help_text()
        sys.exit(0)
    cmd = sys.argv[1].lower()
    if cmd == "list":
        list_queue()
    elif cmd == "approve" and len(sys.argv) == 3:
        approve(int(sys.argv[2]))
    elif cmd == "deny" and len(sys.argv) == 3:
        deny(int(sys.argv[2]))
    else:
        help_text()
