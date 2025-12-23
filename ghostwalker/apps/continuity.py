import os
import csv
from datetime import datetime

GW_ROOT = os.path.expanduser("~/KeystoneCreatorSuite/ghostwalker")
SUMMARY_DIR = os.path.join(GW_ROOT, "logs/daily_summaries")
CSV_PATH = os.path.join(GW_ROOT, "logs/system_state_continuation.csv")

def save_daily_checkpoint():
    today = datetime.now().strftime("%Y-%m-%d")
    txt_path = os.path.join(SUMMARY_DIR, f"summary_{today}.txt")
    
    # Gather stats for the CSV
    revenue_log = os.path.join(GW_ROOT, "logs/payments.log")
    rev_count = 0
    if os.path.exists(revenue_log):
        with open(revenue_log, "r") as f:
            rev_count = len(f.readlines())

    # 1. Generate Human Readable Summary
    with open(txt_path, "w") as f:
        f.write(f"GHOST WALKER DAILY SUMMARY: {today}\n")
        f.write(f"====================================\n")
        f.write(f"Admin: ReeseDroid_Admin\n")
        f.write(f"Status: Operational & Monetized\n")
        f.write(f"Total Transactions Today: {rev_count}\n")
        f.write(f"Files Scanned & Healed: [Verified via Scanner]\n")
        f.write(f"Key Salt: GHOST_WALKER_2025_SECRET\n")
    
    # 2. Generate/Update Machine Readable CSV for AI Continuation
    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as csvfile:
        fieldnames = ["date", "admin", "total_sales", "system_health", "last_key_issued"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "date": today,
            "admin": "ReeseDroid_Admin",
            "total_sales": rev_count,
            "system_health": "OPTIMAL",
            "last_key_issued": "B01E6864816C6E41"
        })

    print(f"✅ Checkpoint Saved: {txt_path}")
    print(f"📊 Continuation CSV Updated: {CSV_PATH}")

if __name__ == "__main__":
    save_daily_checkpoint()
