Payments module implements:
 - MetaMask flow: client sends txHash -> server monitors via RPC and confirms
 - PayPal flow: use PayPal REST API to capture and verify orders (requires ClientID/Secret)
 - License issuance: signed license token generator (HMAC)
