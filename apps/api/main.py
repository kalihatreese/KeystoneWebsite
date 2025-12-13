from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os, json, time, hmac, hashlib, secrets
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, Text, select, insert # <-- Added select, insert
import stripe

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{os.path.expanduser('~/KeystoneCreatorSuite/keystone_store.db')}")
STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

stripe.api_key = STRIPE_KEY

# Use 'sqlite+aiosqlite' for async SQLite
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
metadata = MetaData()

products_table = Table(
    "products", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String, unique=True),
    Column("name", String),
    Column("price_cents", Integer),
    Column("image_url", String),
    Column("description", Text),
    Column("stripe_product_id", String),
    Column("stripe_price_id", String)
)

licenses_table = Table(
    "licenses", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("product_sku", String),
    Column("license_key", String),
    Column("created_at", Integer)
)

app = FastAPI(title="Keystone API - Live")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all) # <-- Correctly using run_sync for synchronous MetaData.create_all

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.get("/api/products")
async def get_products():
    async with AsyncSessionLocal() as session:
        # FIX: Correctly use select() with async session
        stmt = select(products_table)
        res = await session.execute(stmt)
        rows = res.fetchall()
        out = []
        for r in rows:
            out.append({
                # Accessing column by key/attribute works for both ORM and core results
                "sku": r.sku, "name": r.name, "price_cents": r.price_cents,
                "image_url": r.image_url, "description": r.description,
                "stripe_product_id": r.stripe_product_id, "stripe_price_id": r.stripe_price_id
            })
        return {"products": out}

class CheckoutItem(BaseModel):
    stripe_price_id: str
    success_url: str
    cancel_url: str
    customer_email: EmailStr | None = None

@app.post("/api/create-checkout-session")
async def create_checkout_session(item: CheckoutItem):
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe key missing")
    
    # FIX: Get SKU to pass as metadata to the Stripe Session
    sku_to_add = ""
    async with AsyncSessionLocal() as session:
        stmt = select(products_table.c.sku).where(products_table.c.stripe_price_id == item.stripe_price_id)
        res = await session.execute(stmt)
        row = res.fetchone()
        if row:
            sku_to_add = row[0]
        else:
            raise HTTPException(status_code=404, detail="Product price ID not found in database.")

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": item.stripe_price_id, "quantity": 1}],
            mode="payment",
            success_url=item.success_url,
            cancel_url=item.cancel_url,
            customer_email=item.customer_email,
            metadata={"sku": sku_to_add} # <-- Add SKU to metadata
        )
        return {"url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/webhook")
async def webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    event = None
    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {e}")
    else:
        try:
            event = json.loads(payload)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid payload")
    # Handle checkout.session.completed
    etype = getattr(event, "type", None) if not isinstance(event, dict) else event.get("type")
    if etype == "checkout.session.completed":
        data = event["data"]["object"] if isinstance(event, dict) else event.data.object
        customer_email = data.get("customer_details", {}).get("email") or data.get("customer_email")
        sku = data.get("metadata", {}).get("sku","") # Retrieve SKU from metadata
        
        # FIX: create a stronger license key
        key = secrets.token_hex(16)
        
        async with AsyncSessionLocal() as session:
            # FIX: Correctly use insert() with async session
            stmt = insert(licenses_table).values(product_sku=sku, license_key=key, created_at=int(time.time()))
            await session.execute(stmt)
            await session.commit()
            
        # optional email if SMTP configured
        smtp_host = os.getenv("SMTP_HOST","")
        if smtp_host and customer_email:
            try:
                import smtplib
                from email.message import EmailMessage
                smtp_port = int(os.getenv("SMTP_PORT", 587))
                smtp_user = os.getenv("SMTP_USER","")
                smtp_pass = os.getenv("SMTP_PASS","")
                from_addr = os.getenv("FROM_EMAIL", smtp_user or "no-reply@keystoneaiml.com")
                msg = EmailMessage()
                msg["Subject"] = "Your Keystone purchase"
                msg["From"] = from_addr
                msg["To"] = customer_email
                msg.set_content(f"Thanks. Your license: {key}")
                s = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
                s.starttls()
                if smtp_user and smtp_pass:
                    s.login(smtp_user, smtp_pass)
                s.send_message(msg)
                s.quit()
            except Exception as e:
                print("Email send failed:", e)
    return JSONResponse({"status":"ok"})
