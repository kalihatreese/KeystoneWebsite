#!/usr/bin/env python3
import os, json, stripe, sqlite3, sys
stripe.api_key = os.getenv("STRIPE_SECRET_KEY","")
BASE = os.path.expanduser("~/KeystoneCreatorSuite")
DB = os.path.expanduser("~/KeystoneCreatorSuite/keystone_payments.db")
if not stripe.api_key:
    print("[!] STRIPE_SECRET_KEY missing in env; will only write local mapping.")
# find products file
candidates = [
    os.path.join(BASE,"data","products.json"),
    os.path.join(BASE,"products.json"),
    os.path.join(BASE,"keystone-storefront","products.json"),
    os.path.join(BASE,"Autotrend_vault","products.json"),
    os.path.join(BASE,"liveProducts.json")
]
products_file = None
for p in candidates:
    if os.path.isfile(p):
        products_file = p
        break
if not products_file:
    print("[!] No products.json found. Create one at ~/KeystoneCreatorSuite/data/products.json and re-run.")
    sys.exit(1)
with open(products_file) as fh:
    prods = json.load(fh)
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products (sku TEXT PRIMARY KEY, name TEXT, price_cents INTEGER, stripe_product_id TEXT, stripe_price_id TEXT, image_url TEXT, description TEXT)''')
conn.commit()
for p in prods:
    sku = p.get("sku") or p.get("id")
    name = p.get("name") or sku
    price_cents = int(round(float(p.get("price", p.get("price_usd",0))) * 100))
    image = p.get("image_url","")
    desc = p.get("description","")
    cur = c.execute("SELECT stripe_product_id,stripe_price_id FROM products WHERE sku=?", (sku,)).fetchone()
    if cur and cur[0]:
        print("[~] already synced:", sku)
        continue
    try:
        if stripe.api_key:
            prod = stripe.Product.create(name=name, description=desc, images=[image] if image else [])
            price = stripe.Price.create(product=prod.id, unit_amount=price_cents, currency="usd")
            stripe_product_id = prod.id
            stripe_price_id = price.id
            print("[+] Stripe:", sku, name, f"${price_cents/100:.2f}", stripe_price_id)
        else:
            stripe_product_id = ""
            stripe_price_id = ""
        c.execute("INSERT OR REPLACE INTO products (sku,name,price_cents,stripe_product_id,stripe_price_id,image_url,description) VALUES (?,?,?,?,?,?,?)",
                  (sku,name,price_cents,stripe_product_id,stripe_price_id,image,desc))
        conn.commit()
    except Exception as e:
        print("[!] error for", sku, e)
conn.close()
print("[*] Done. DB:", DB)
