"""
core/defensive.py
Safety checks and a human-approval mechanism for risky actions.
This module deliberately does NOT execute or mutate code itself.
"""
import re
import json
import os
import logging
from typing import Tuple

APPROVAL_FILE = "core/approval_queue.json"
BANNED_PATTERNS = [
    r"kill process", r"format /", r"rm -rf /", r"self-?delete", r"self-?destruct",
    r"bypass", r"privilege escalation", r"exploit", r"dd if=", r"shutdown -h now"
]

def is_safe_input(text: str) -> Tuple[bool, str]:
    """Return (safe, reason). False if banned pattern found."""
    lowered = text.lower()
    for p in BANNED_PATTERNS:
        if re.search(p, lowered):
            return False, f"Matches banned pattern: {p}"
    # length / suspicious checks (simple heuristics)
    if len(text) > 10000:
        return False, "Input too long"
    return True, "ok"

def queue_for_approval(action: dict) -> None:
    """Append an action dict to the approval queue for a human reviewer."""
    q = []
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, "r", encoding="utf-8") as f:
                q = json.load(f)
        except Exception:
            q = []
    q.append(action)
    with open(APPROVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)
    logging.info(f"Defensive: queued action for human approval: {action.get('id','<no-id>')}")

def requires_approval(action: dict) -> bool:
    """
    Simple policy: structural changes, writes to critical paths, and self-modify requests
    must be human-approved. This function decides whether approval is required.
    """
    kind = action.get("kind","").lower()
    if kind in ("mutate_core", "self_modify", "deploy_service", "modify_cop"):
        return True
    # high-risk flags
    if action.get("risk","") in ("high", "critical"):
        return True
    return False

def list_approvals() -> list:
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

# notify on queue (best-effort; optional)
try:
    from core.notify import notify_approval_queued
except Exception:
    notify_approval_queued = None

def queue_for_approval(action: dict) -> None:
    \"\"\"Append an action dict to the approval queue for a human reviewer.\"\"\"
    q = []
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, "r", encoding="utf-8") as f:
                q = json.load(f)
        except Exception:
            q = []
    q.append(action)
    with open(APPROVAL_FILE, "w", encoding="utf-8") as f:
        json.dump(q, f, indent=2)
    logging.info(f"Defensive: queued action for human approval: {action.get('id','<no-id>')}")
    # notify admin (best-effort)
    try:
        if notify_approval_queued:
            notify_approval_queued(action)
    except Exception:
        pass
