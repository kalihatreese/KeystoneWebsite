import os, time, stripe
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

STRIPE_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_test_REPLACE_ME")
PRODUCT_NAME = "Ghostwalker Digital Access"
PRICE_CENTS = 2500  # $25

stripe.api_key = STRIPE_KEY

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <h1>Ghostwalker</h1>
    <p>Digital access package</p>
    <form action="/checkout" method="post">
        <button type="submit">Buy Now – $25</button>
    </form>
    """

@app.post("/checkout")
def checkout():
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": PRODUCT_NAME},
                "unit_amount": PRICE_CENTS,
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8080/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8080/cancel",
    )
    return {"url": session.url}

@app.get("/success")
def success(session_id: str):
    filename = "ghostwalker.zip"
    path = os.path.join("downloads", filename)
    return FileResponse(path, filename=filename)

@app.get("/cancel")
def cancel():
    return {"status": "cancelled"}
