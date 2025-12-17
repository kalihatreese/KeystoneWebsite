#!/data/data/com.termux/files/usr/bin/bash
source /data/data/com.termux/files/home/Ashleyana/.venv/bin/activate
nohup python3 /data/data/com.termux/files/home/Ashleyana/lab/auto_store_manager.py > /data/data/com.termux/files/home/Ashleyana/lab/manager.log 2>&1 &
nohup uvicorn local_app:app --host 0.0.0.0 --port 8000 > /data/data/com.termux/files/home/Ashleyana/server.log 2>&1 &
