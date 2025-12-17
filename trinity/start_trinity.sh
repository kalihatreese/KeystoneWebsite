#!/data/data/com.termux/files/usr/bin/bash
# Keep Trinity alive on ReeseOS boot

# Acquire wake lock to prevent phone sleep
termux-wake-lock

# Navigate to Trinity folder
cd ~/KeystoneCreatorSuite/trinity

# Start PM2 (resurrect previous processes or start fresh)
pm2 resurrect || pm2 start index.js --name trinity --watch \
--output ~/KeystoneCreatorSuite/trinity/logs/out.log \
--error ~/KeystoneCreatorSuite/trinity/logs/err.log

# Save current PM2 process list
pm2 save
