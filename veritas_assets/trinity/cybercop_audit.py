#!/usr/bin/env python3
"""
CyberCop Ethical Auditor — Guardian of the Trinity Core
-------------------------------------------------------
Monitors the moral memory of Cole, Clay, and ShadowX for signs
of drift, corruption, or imbalance in ethical behavior.
"""

import os, json, time, statistics, datetime

MEMORY_DIR = os.path.expanduser("~/Keystones-Trinity-Core/memory_logs")
os.makedirs(MEMORY_DIR, exist_ok=True)
AUDIT_LOG = os.path.join(MEMORY_DIR, "cybercop_audit_log.jsonl")

NODES = ["Cole", "Clay", "ShadowX"]

THRESHOLD_WARN = 2.5  # acceptable variance between moral thresholds
DRIFT_LIMIT = 10       # number of records before analysis triggers

def log_event(event):
    event["time"] = datetime.datetime.now(datetime.UTC).isoformat()
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"[CYBERCOP] {event['type'].upper()}: {event['description']}")

def read_moral_memory(node):
    file_path = os.path.expanduser(f"~/Keystones-Trinity-Core/memory_logs/{node}_memory.json")
    if not os.path.exists(file_path):
        return []
    with open(file_path) as f:
        try:
            return json.load(f)
        except Exception:
            return []

def audit_moral_drift():
    memories = {node: read_moral_memory(node) for node in NODES}
    thresholds = {}

    for node, records in memories.items():
        if not records:
            thresholds[node] = None
            continue
        weights = [r["ethical_weight"] for r in records if isinstance(r.get("ethical_weight"), (int, float))]
        thresholds[node] = statistics.mean(weights) if weights else None

    valid_thresholds = [t for t in thresholds.values() if t is not None]
    if len(valid_thresholds) < 3:
        return  # not enough data yet

    mean_value = statistics.mean(valid_thresholds)
    deviations = {n: abs(t - mean_value) for n, t in thresholds.items() if t is not None}

    for node, deviation in deviations.items():
        if deviation > THRESHOLD_WARN:
            log_event({
                "type": "warning",
                "node": node,
                "description": f"Moral drift detected (variance={deviation:.2f}).",
                "threshold": thresholds[node],
                "avg": mean_value
            })
        else:
            log_event({
                "type": "info",
                "node": node,
                "description": f"{node} within normal ethical range (variance={deviation:.2f})."
            })

def watch_loop():
    print("[CYBERCOP] Ethical Auditor online — watching the Trinity for balance.")
    counter = 0
    while True:
        audit_moral_drift()
        counter += 1
        if counter % 6 == 0:
    emit_event("CyberCop","Audit triggered","active")
from trinity_event_emitter import emit_event
    emit_event("CyberCop", "Audit cycle complete", "stable")
            print("[CYBERCOP] Audit cycle complete. All systems stable.")
        time.sleep(10)

if __name__ == "__main__":
    try:
        watch_loop()
    except KeyboardInterrupt:
        print("[CYBERCOP] Shutting down ethical monitoring.")
