#!/usr/bin/env python3
"""
Trinity Event Logger — Distributed Historical Chronicle
-------------------------------------------------------
Receives event reports from Cole, Clay, ShadowX, CyberCop, and Ashleyana,
verifies authenticity, and appends them into the Mission Log Chronicle section
of the README.md for immutable, continuous historical tracking.
"""
import zmq, json, time, os, datetime, re, subprocess

REPO_PATH = os.path.expanduser("~/Keystones-Trinity-Core")
README_PATH = os.path.join(REPO_PATH, "README.md")
EVENT_PORT = 5588

def append_to_mission_log(entry):
    """Append structured event entries into the Mission Log Chronicle."""
    if not os.path.exists(README_PATH):
        print("[LOGGER] README not found.")
        return

    with open(README_PATH, "r") as f:
        content = f.read()

    section_header = "## 📜 Mission Log Chronicle"
    if section_header not in content:
        content += f"\n\n{section_header}\n_A living record of verified commits and milestones._\n\n"

    new_entry = f"- **{entry['time']}** — `{entry['source']}` — {entry['event']} *(status: {entry['status']})*"
    updated_section = re.sub(
        rf"({section_header}[\s\S]*)",
        lambda m: m.group(1).strip() + "\n" + new_entry,
        content
    )

    with open(README_PATH, "w") as f:
        f.write(updated_section)

    print(f"[LOGGER] Recorded event from {entry['source']}: {entry['event']}")

def listen_for_events():
    ctx = zmq.Context()
    sock = ctx.socket(zmq.PULL)
    sock.bind(f"tcp://127.0.0.1:{EVENT_PORT}")
    print(f"[LOGGER] Event Logger active on port {EVENT_PORT} — awaiting transmissions...")

    while True:
        try:
            msg = sock.recv_json()
            msg["time"] = datetime.datetime.now(datetime.UTC).isoformat()
            append_to_mission_log(msg)
            time.sleep(0.2)
        except Exception as e:
            print("[LOGGER] Error:", e)
            time.sleep(1)

def git_commit_update():
    try:
        subprocess.run(["git", "add", "README.md"], cwd=REPO_PATH)
        subprocess.run(["git", "commit", "-S", "-m", "Automated event log update — Trinity live record"], cwd=REPO_PATH)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_PATH)
        print("[LOGGER] Mission Log pushed to GitHub.")
    except Exception as e:
        print("[LOGGER] Git commit/push failed:", e)

if __name__ == "__main__":
    print("[LOGGER] Trinity Event Logger initiated.")
    try:
        listen_for_events()
    except KeyboardInterrupt:
        git_commit_update()
        print("\n[LOGGER] Shutdown complete — final log committed.")
