#!/bin/bash

# Trinity Multi-Invoice Injector
BASE_URL="http://localhost:3001"
NUM_INVOICES=5  # number of invoices to create

# Define chains you want to test
CHAINS=("ETH" "BSC" "POLYGON")

echo "🔥 Starting multi-invoice injection..."

for i in $(seq 1 $NUM_INVOICES); do
  AMOUNT=$((RANDOM % 500 + 1))  # Random amount between 1 and 500
  CHAIN=${CHAINS[$RANDOM % ${#CHAINS[@]}]}
  DESCRIPTION="Auto Invoice #$i on $CHAIN"

  RESPONSE=$(curl -s -X POST "$BASE_URL/create-invoice" \
    -H "Content-Type: application/json" \
    -d "{\"amount\":$AMOUNT,\"currency\":\"$CHAIN\",\"description\":\"$DESCRIPTION\"}")

  ID=$(echo "$RESPONSE" | jq -r '.id')
  STATUS=$(echo "$RESPONSE" | jq -r '.status')

  echo "✅ Created Invoice #$i | ID: $ID | Amount: $AMOUNT | Chain: $CHAIN | Status: $STATUS"
done

echo -e "\n📄 Listing all invoices after injection..."
curl -s "$BASE_URL/api/invoices" | jq
