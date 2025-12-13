#!/bin/bash

BASE_URL="http://localhost:3001"
LOG_FILE="invoice_injection.log"

CHAINS=("ETH" "BSC" "POLYGON")
AMOUNT=25
COUNT=0

echo "=== Trinity Invoice Injection Started ===" | tee -a "$LOG_FILE"
echo "Time: $(date)" | tee -a "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

while true; do
  CHAIN=${CHAINS[$((COUNT % ${#CHAINS[@]}))]}
  TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

  RESPONSE=$(curl -s -X POST "$BASE_URL/create-invoice" \
    -H "Content-Type: application/json" \
    -d "{\"amount\":$AMOUNT,\"chain\":\"$CHAIN\",\"description\":\"Auto Inject $CHAIN $TIMESTAMP\"}")

  echo "[$TIMESTAMP] Injected $CHAIN invoice | Amount: $AMOUNT | Response: $RESPONSE" | tee -a "$LOG_FILE"

  COUNT=$((COUNT + 1))
  AMOUNT=$((AMOUNT + 5))

  sleep 3
done
