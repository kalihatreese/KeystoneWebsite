from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")  # set this in .env
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.mount("/", StaticFiles(directory="build", html=True), name="frontend")

@app.post("/api/create-checkout-session")
async def create_checkout():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Keystone AI Stack Subscription'},
                    'unit_amount': 99900,  # $999.00
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:3000/success.html',
            cancel_url='http://localhost:3000/cancel.html',
        )
        return JSONResponse({'url': session.url})
    except Exception as e:
        return JSONResponse({'error': str(e)})

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Keystone + Veritas live"}
