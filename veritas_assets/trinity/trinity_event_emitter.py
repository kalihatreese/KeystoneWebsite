#!/usr/bin/env python3
"""
Trinity Event Emitter — Node Communication Helper
-------------------------------------------------
Allows any subsystem (Cole, Clay, ShadowX, CyberCop, Ashleyana)
to publish verified event messages to the Trinity Event Logger.
"""

import zmq, json, datetime

EVENT_PORT = 5588

def emit_event(source, event, status="ok"):
    """Send a structured JSON event to the Trinity Event Logger."""
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUSH)
    sock.connect(f"tcp://127.0.0.1:{EVENT_PORT}")

    payload = {
        "source": source,
        "event": event,
        "status": status,
        "timestamp": datetime.datetime.now(datetime.UTC).isoformat()
    }
    try:
        sock.send_json(payload)
        print(f"[{source}] → Event sent: {event} ({status})")
    except Exception as e:
        print(f"[{source}] Event send failed: {e}")
    finally:
        sock.close()
        ctx.term()

# Direct test
if __name__ == "__main__":
    emit_event("Clay", "Trinity synchronization heartbeat", "verified")
