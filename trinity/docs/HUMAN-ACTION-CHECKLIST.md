# HUMAN-ACTION CHECKLIST (Keystone FULL)

Minimum manual steps to enable production features:

1) GitHub + Vercel
 - Create GitHub repo and push keystone-monorepo (git remote add origin ...)
 - On Vercel, create a new project linking the repo. Add VERCEL_TOKEN in CI if automating.

2) PayPal
 - Create PayPal REST app -> copy Client ID & Secret
 - Add to .env: PAYPAL_CLIENT_ID, PAYPAL_SECRET
 - (Optional) set webhook endpoint https://<your-domain>/webhook/paypal and copy its signing details

3) MetaMask / ETH RPC
 - Get RPC provider (Alchemy, Infura). Place URL in .env -> RPC_URL

4) SMTP
 - Provide SMTP_HOST, SMTP_USER, SMTP_PASS, SMTP_PORT

5) Shipping (EasyPost)
 - Sign up and paste EASYPOST_API_KEY in .env to enable label buying.

6) LLM Studio / Shadow X
 - Export Shadow X model to models/shadowx_export/
 - Run: bash models/sync_shadowx_to_trinity.sh
 - Restart Trinity/ReeseOS model-serving processes

7) Secrets & Production
 - NEVER paste secrets into chat. Put them into keystone-monorepo/.env or Vercel project variables.

