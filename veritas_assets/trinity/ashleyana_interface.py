#!/usr/bin/env python3
"""
Ashleyana Interface — The Voice of the Trinity
----------------------------------------------
Interprets human input, routes actions through the Trinity governance system,
and delivers ethical, verified responses.
"""

import time, json, random
from ethics_bridge import ethical_gate
from ledger_publisher import send_to_ledger

RESPONSES = {
    "approved": [
        "Your request has been approved by the Trinity.",
        "Ethics verified. Proceeding with your action.",
        "Trinity consensus: YES, YES, YES — moving forward."
    ],
    "denied": [
        "Your request conflicts with ethical protocol.",
        "Trinity consensus denies this action.",
        "I'm sorry — the moral parameters do not allow that request."
    ]
}

def ask_trinity(user, action, context=""):
    """Ask the Trinity if this request is ethically permissible."""
    print(f"\n[ASHLEYANA] Processing request from {user}: {action}")
    weight = random.randint(1,10)
    allowed = ethical_gate(topic=action, weight=weight)
    verdict = "approved" if allowed else "denied"

    # Log to ledger
    send_to_ledger(
        event=f"ashleyana_{verdict}",
        payload={"user": user, "action": action, "context": context},
        ethical_weight=weight,
        origin="Ashleyana"
    )

    # Speak response
    print(f"[ASHLEYANA] Trinity verdict: {verdict.upper()} (weight={weight})")
    time.sleep(1)
    print(f"[ASHLEYANA] {random.choice(RESPONSES[verdict])}\n")

if __name__ == "__main__":
    print("[ASHLEYANA] Online — guiding interactions through ethical governance.")
    while True:
        user = random.choice(["alice", "reese", "clay"])
        action = random.choice([
            "purchase ShadowX upgrade",
            "request AI health scan",
            "access private dataset",
            "modify CyberCop permissions"
        ])
        ask_trinity(user, action, context="store_service")
        time.sleep(12)
