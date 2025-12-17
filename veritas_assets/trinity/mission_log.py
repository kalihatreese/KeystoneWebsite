#!/usr/bin/env python3
"""
Mission Log Chronicle — Auto-Documentation System
-------------------------------------------------
Pulls recent git commit data and appends it to the README.md
under the '📜 Mission Log Chronicle' section. Keeps the
Trinity Core repository self-documenting and historically verifiable.
"""
import subprocess, datetime, os, re

REPO_PATH = os.path.expanduser("~/Keystones-Trinity-Core")
README_PATH = os.path.join(REPO_PATH, "README.md")

def get_git_log(limit=5):
    """Fetch recent git commits with message, hash, and date."""
    cmd = ["git", "-C", REPO_PATH, "log", f"-{limit}", "--pretty=format:%h|%an|%ad|%s", "--date=iso"]
    output = subprocess.check_output(cmd, text=True)
    entries = []
    for line in output.strip().split("\n"):
        try:
            commit_hash, author, date, message = line.split("|", 3)
            entries.append({
                "hash": commit_hash,
                "author": author,
                "date": date,
                "message": message
            })
        except ValueError:
            pass
    return entries

def update_readme(entries):
    """Append or update Mission Log section in README."""
    with open(README_PATH, "r") as f:
        content = f.read()

    section_header = "## 📜 Mission Log Chronicle"
    if section_header not in content:
        content += f"\n\n{section_header}\n"
        content += "_A living record of verified commits and milestones._\n\n"

    log_entries = []
    for e in entries:
        log_entries.append(f"- **{e['date']}** — `{e['hash']}` — {e['message']} *(by {e['author']})*")

    new_section = section_header + "\n_A living record of verified commits and milestones._\n\n" + "\n".join(log_entries) + "\n"
    content = re.sub(rf"{section_header}[\s\S]*", new_section, content)

    with open(README_PATH, "w") as f:
        f.write(content)

def main():
    entries = get_git_log(limit=8)
    update_readme(entries)
    print("[MISSION LOG] README updated with latest commit history.")

if __name__ == "__main__":
    main()
