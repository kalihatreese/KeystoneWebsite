#!/data/data/com.termux/files/usr/bin/sh
pm2 resurrect >/dev/null 2>&1 || pm2 start all >/dev/null 2>&1
pm2 save >/dev/null 2>&1
