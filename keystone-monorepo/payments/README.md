Payments module (auto-created).
Files:
- webhook.py            FastAPI webhook endpoint (/webhook). Run with uvicorn payments.webhook:app --port 9000
- license.py            Simple license generator & local store
- sync_products_to_stripe.py   Sync products JSON to Stripe & store mapping in SQLite
- run_payments_local.sh Start webhook in background and log to ~/KeystoneCreatorSuite/payments_webhook.log

ENV needed (place in ~/KeystoneCreatorSuite/keys/*.env*):
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=   # set after creating webhook in Stripe (recommended)
SMTP_HOST=... (optional)
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
FROM_EMAIL=

To sync products (creates Stripe Product + Price if STRIPE_SECRET_KEY is set):
~/KeystoneCreatorSuite/keystone-monorepo/payments/sync_products_to_stripe.py

To run webhook locally:
~/KeystoneCreatorSuite/keystone-monorepo/payments/run_payments_local.sh

