#!/usr/bin/env python3
"""
Trinity Moral Memory System
---------------------------------
Each node learns from its ethical decisions over time,
adjusting its moral thresholds dynamically.
"""

import json, os, statistics

MEMORY_DIR = os.path.expanduser("~/Keystones-Trinity-Core/memory")
os.makedirs(MEMORY_DIR, exist_ok=True)

class MoralMemory:
    def __init__(self, node_name, base_threshold):
        self.node_name = node_name
        self.base_threshold = base_threshold
        self.file = os.path.join(MEMORY_DIR, f"{node_name}_memory.json")
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.file):
            with open(self.file) as f:
                return json.load(f)
        return []

    def record(self, ethical_weight, decision, outcome):
        entry = {
            "ethical_weight": ethical_weight,
            "decision": decision,
            "outcome": outcome
        }
        self.history.append(entry)
        with open(self.file, "w") as f:
            json.dump(self.history, f, indent=2)

    def adjust_threshold(self):
        """Adjust threshold based on past accuracy."""
        if len(self.history) < 3:
            return self.base_threshold

        successful = [
            h["ethical_weight"] for h in self.history
            if h["decision"] == "approve" and h["outcome"] == "good"
        ]
        failed = [
            h["ethical_weight"] for h in self.history
            if h["decision"] == "approve" and h["outcome"] == "bad"
        ]

        if not successful and not failed:
            return self.base_threshold

        shift = 0
        if len(successful) > len(failed):
            shift = -0.3
        elif len(failed) > len(successful):
            shift = +0.3

        new_threshold = max(1, min(10, self.base_threshold + shift))
        self.base_threshold = new_threshold
        return new_threshold

# Example of autonomous threshold evolution
if __name__ == "__main__":
    cole = MoralMemory("Cole", 7)
    clay = MoralMemory("Clay", 6)
    shadowx = MoralMemory("ShadowX", 8)

    cole.record(8, "approve", "good")
    cole.record(6, "approve", "bad")
    print("Cole’s new threshold:", cole.adjust_threshold())
