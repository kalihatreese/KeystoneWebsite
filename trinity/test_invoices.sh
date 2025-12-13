#!/bin/bash

# Quick Trinity API test script

BASE_URL="http://localhost:3001"

echo "✅ Testing Health Route..."
curl -s "$BASE_URL/health" | jq

echo -e "\n✅ Testing Register Route..."
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq

echo -e "\n✅ Creating Invoice..."
curl -s -X POST "$BASE_URL/create-invoice" \
  -H "Content-Type: application/json" \
  -d '{"amount":100,"currency":"ETH","description":"Test Invoice"}' | jq

echo -e "\n✅ Listing All Invoices..."
curl -s "$BASE_URL/api/invoices" | jq

