#!/bin/bash
set -a
source ~/KeystoneCreatorSuite/.env
set +a

PRIMARY="BTCUSD"
SCAN_LIST=("ETHUSD" "SOLUSD" "SPY" "QQQ" "AAPL" "NVDA")

log() {
    echo "[Trinity] $1"
}

log "Booting Trinity Dual‑Mode Engine..."
log "Using API keys already loaded from .env"

while true; do
    log "Evaluating primary symbol: $PRIMARY"
    primary_signal=$(python3 ~/Keystone/Trinity/signal_primary.py "$PRIMARY")

    best_symbol="$PRIMARY"
    best_signal="$primary_signal"
    log "Primary Signal: $primary_signal"

    for sym in "${SCAN_LIST[@]}"; do
        sig=$(python3 ~/Keystone/Trinity/signal_scan.py "$sym")
        log "Scan $sym → $sig"

        if (( $(echo "$sig > $best_signal" | bc -l) )); then
            best_signal="$sig"
            best_symbol="$sym"
            log "New leader: $best_symbol ($best_signal)"
        fi
    done

    log "Executing trade on: $best_symbol"
    python3 ~/Keystone/Trinity/execute.py "$best_symbol" "$best_signal"

    sleep 60
done
