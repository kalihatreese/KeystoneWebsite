#!/usr/bin/env python3
"""
Trinity Integration Layer — Consensus ↔ Moral Memory
----------------------------------------------------
Connects trinity_consensus.py and trinity_memory.py so
each node learns from its decisions in real time.
"""

import os, json, random
from trinity_memory import MoralMemory

MEMORY_MAP = {
    "Cole": MoralMemory("Cole", 7),
    "Clay": MoralMemory("Clay", 6),
    "ShadowX": MoralMemory("ShadowX", 8)
}

def simulate_decision(topic, ethical_weight):
    """Simulate a Trinity Consensus and record outcomes."""
    print(f"\n[TRINITY] New ethical decision proposed: '{topic}' (weight={ethical_weight})")

    votes = {}
    for node, memory in MEMORY_MAP.items():
        threshold = memory.adjust_threshold()
        decision = "approve" if ethical_weight <= threshold else "deny"
        votes[node] = decision
        print(f" - {node} (threshold={threshold:.2f}) → {decision}")

    # Determine consensus (must be unanimous)
    consensus = len(set(votes.values())) == 1 and list(votes.values())[0] == "approve"
    result = "APPROVED" if consensus else "REJECTED"
    print(f"[TRINITY] Final consensus: {result}")

    # Randomly simulate moral outcome (good/bad) — placeholder for real evaluation
    outcome = random.choice(["good", "bad"]) if result == "APPROVED" else "neutral"

    # Record and update each node’s moral memory
    for node, memory in MEMORY_MAP.items():
        memory.record(ethical_weight, votes[node], outcome)
        memory.adjust_threshold()

    print(f"[MEMORY] Recorded decision with outcome='{outcome}' across all nodes.\n")

if __name__ == "__main__":
    simulate_decision("AI surveillance ethics review", 7)
    simulate_decision("Medical data sharing consent", 5)
    simulate_decision("Autonomous defense protocol", 9)
