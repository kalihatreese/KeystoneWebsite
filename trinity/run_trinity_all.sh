#!/bin/bash
# Start Trinity server with PM2

# Ensure PM2 is installed globally
command -v pm2 >/dev/null 2>&1 || npm install -g pm2

# Start or restart Trinity
pm2 start index.js --name trinity --watch

# Save PM2 process list for auto-start
pm2 save
