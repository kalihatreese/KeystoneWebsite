#!/data/data/com.termux/files/usr/bin/bash
# Startup script for Trinity + Veritas

# Wait a bit for network and storage
sleep 10

cd ~/KeystoneCreatorSuite/trinity

# Kill any old node processes on port 3001
PID=$(lsof -t -i:3001)
if [ ! -z "$PID" ]; then
  kill -9 $PID
fi

# Start Trinity in background with logging
nohup node index.js > veritas.log 2>&1 &
echo "Trinity started, logging to veritas.log"
