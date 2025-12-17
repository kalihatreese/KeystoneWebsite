#!/data/data/com.termux/files/usr/bin/bash
echo "=========================================="
echo "        ✨ TRINITY SYSTEM DASHBOARD ✨"
echo "=========================================="
echo ""
echo "  [1] Mesh Heartbeats  (Cole, Clay, ShadowX)"
echo "  [2] CyberCop Ethics Watch"
echo "  [3] Ashleyana Bridge Activity"
echo "  [4] Ledger Records"
echo "  [5] Exit"
echo ""
read -p "Select a log to view live: " choice
case $choice in
  1) tail -f logs/mesh.log ;;
  2) tail -f logs/cybercop.log ;;
  3) tail -f logs/ashleyana_bridge.log ;;
  4) tail -f logs/ledger.log ;;
  5) echo "Goodbye, Overseer." && exit ;;
  *) echo "Invalid selection." ;;
esac
