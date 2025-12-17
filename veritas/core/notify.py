#!/usr/bin/env python3
"""
core/notify.py
Lightweight notification; writes alerts to core/notifications.log.
Replace notify_admin() with real email/SMS/Push integrations if desired.
"""
import os
import time
import json

NOTIF_LOG = "core/notifications.log"

def notify_admin(subject: str, body: str, meta: dict = None):
    """Append a notification entry to the notifications log."""
    entry = {
        "ts": time.time(),
        "subject": subject,
        "body": body,
        "meta": meta or {}
    }
    try:
        with open(NOTIF_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print("Notify error:", e)
    # Placeholder print to surface notification immediately
    print(f"[NOTIFY] {subject} - {body[:200]}")

# Small helper to summarize approval action for notification
def notify_approval_queued(action: dict):
    subj = f"Approval queued: {action.get('kind','<unknown>')} id={action.get('id','<no-id>')}"
    body = action.get('description','(no description)')
    notify_admin(subj, body, {"id": action.get("id")})
