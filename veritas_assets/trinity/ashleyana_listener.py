#!/usr/bin/env python3
"""
Ashleyana Listener — Human-Readable Ledger Stream
-------------------------------------------------
Watches ledger.jsonl for new records and prints them with friendly context.
This file does NOT take action; it only displays information.
"""

import os, time, json

LEDGER_PATH = os.path.expanduser("~/Keystones-Trinity-Core/ledger.jsonl")

def tail_ledger():
    print("[ASHLEYANA LISTENER] Monitoring ledger for new activity…")
    seen = 0
    while True:
        try:
            if not os.path.exists(LEDGER_PATH):
                time.sleep(2)
                continue
            with open(LEDGER_PATH) as f:
                lines = f.readlines()
            if len(lines) > seen:
                for line in lines[seen:]:
                    try:
                        entry = json.loads(line)
                        event = entry.get("event","(unknown)")
                        origin = entry.get("origin","(unknown)")
                        timestamp = entry.get("timestamp","")
                        print(f"[ASHLEYANA] {timestamp} :: {origin} reported → {event}")
                    except Exception:
                        print("[ASHLEYANA] unreadable entry.")
                seen = len(lines)
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n[ASHLEYANA LISTENER] stopped by user.")
            break
        except Exception as e:
            print(f"[ASHLEYANA LISTENER] Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    tail_ledger()
