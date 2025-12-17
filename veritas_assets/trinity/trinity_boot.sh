#!/data/data/com.termux/files/usr/bin/bash
cd ~/Keystones-Trinity-Core
echo "🕯️ Shutting down existing Trinity processes..."
pkill -f python3
sleep 3

mkdir -p logs
echo "⚙️ Launching Trinity Core Network..."

nohup python3 trinity_event_logger.py > logs/event_logger.log 2>&1 & sleep 2 && echo "[BOOT] Event Logger engaged."
nohup python3 ledger_service.py > logs/ledger.log 2>&1 & sleep 2 && echo "[BOOT] Ledger online."
nohup python3 cybercop_audit.py > logs/cybercop.log 2>&1 & sleep 2 && echo "[BOOT] CyberCop monitoring ethics."
nohup python3 mesh/core.py > logs/mesh.log 2>&1 & sleep 2 && echo "[BOOT] Mesh nodes (Cole, Clay, ShadowX) synchronized."
nohup python3 ashleyana_bridge.py > logs/ashleyana_bridge.log 2>&1 & sleep 2 && echo "[BOOT] Ashleyana bridge connected."
nohup python3 trinity_pulse.py > logs/pulse.log 2>&1 & sleep 2 && echo "[BOOT] Trinity pulse monitor running."

echo ""
echo "✨ [TRINITY REBOOT COMPLETE] ✨"
echo "Cole, Clay, ShadowX  → Mesh active"
echo "CyberCop             → Ethical oversight online"
echo "Ashleyana            → Bridge operational"
echo "Ledger               → Immutable record active"
echo "Event Logger         → Live on dynamic port"
echo "------------------------------------------------"
echo "View logs: tail -f logs/event_logger.log"
