from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os, json, time, hmac, hashlib
import stripe
from .license import create_license_for_session

app = FastAPI(title="Keystone Payments Webhook")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

@app.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig = request.headers.get("stripe-signature", "")
    event = None
    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {e}")
    else:
        # best-effort parse (only for dev)
        try:
            event = json.loads(payload)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid payload")

    etype = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)

    if etype == "checkout.session.completed":
        data = event["data"]["object"] if isinstance(event, dict) else event.data.object
        # create license(s)
        session_id = data.get("id") if isinstance(data, dict) else getattr(data, "id", "unknown")
        metadata = data.get("metadata", {}) if isinstance(data, dict) else getattr(data, "metadata", {})
        sku = metadata.get("sku", "")
        lic = create_license_for_session(session_id=session_id, sku=sku)
        # optionally email customer (left as TODO for SMTP env)
        return JSONResponse({"status":"license_created", "license": lic})
    return JSONResponse({"status":"ignored", "type": etype})
