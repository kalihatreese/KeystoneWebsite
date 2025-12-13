#!/usr/bin/env bash
set -euo pipefail
ROOT="$PWD"
MONO="$ROOT/keystone-monorepo"
BACKUP="${MONO}.backup.$(date +%s)"

# Backup existing if present
if [ -d "$MONO" ]; then
  echo "Backing up existing keystone-monorepo -> $BACKUP"
  cp -a "$MONO" "$BACKUP"
fi

mkdir -p "$MONO"
cd "$MONO"

# ensure base scaffold exists; if not, create minimal skeleton
if [ ! -d "./apps" ]; then
  echo "Base scaffold missing - generating minimal base (api + frontend + infra)"
  mkdir -p apps/api apps/frontend infra bootstrap docs models payments serverless admin
  # simple placeholders
  echo "FastAPI placeholder" > apps/api/main.py
  echo "Next.js placeholder" > apps/frontend/README.md
fi

# Write .env.example (do not overwrite existing .env)
cat > .env.example <<'ENV'
# Keystone full stack .env.example
PORT=3000
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
MERCHANT_ADDRESS=0xc22f0db6ba4935083e9d69a5defd7c32d76228bf
CONFIRMATIONS=3

# PayPal (HUMAN ACTION)
PAYPAL_CLIENT_ID=
PAYPAL_SECRET=

# Stripe (optional)
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# SMTP for receipts/alerts (HUMAN ACTION)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
ADMIN_EMAIL=kalihatreese@gmail.com

# EasyPost / Shippo (optional, HUMAN ACTION)
EASYPOST_API_KEY=
SHIPPO_API_KEY=

# GitHub/Vercel automation (HUMAN ACTION if you want autodeploy)
GITHUB_REPO_URL=
VERCEL_TOKEN=
VERCEL_PROJECT_ID=
ENV

# Create serverless API (Vercel style) for payments and order verify
mkdir -p serverless/api
cat > serverless/api/orders.js <<'JS'
/**
 * Vercel Serverless endpoint: /api/orders
 * POST payload for ETH payments:
 * { txHash, productId, priceEth, buyerEmail, truthPass }
 * POST payload for PayPal callback: { method: 'paypal', orderID, productId, buyerEmail }
 *
 * This endpoint validates the payload and writes a basic JSON order to /tmp/orders.json
 * In production this should call your central DB and verify PayPal via REST API and ETH via RPC.
 */
const fs = require('fs');
const path = require('path');

module.exports = async (req, res) => {
  try {
    const body = req.body || (await new Promise(r => { let d=''; req.on('data',c=>d+=c); req.on('end',()=>r(JSON.parse(d||'{}'))); }));
    const ordersFile = path.join('/tmp','keystone_orders.json');
    const orders = fs.existsSync(ordersFile) ? JSON.parse(fs.readFileSync(ordersFile,'utf8')) : [];
    const now = new Date().toISOString();
    const id = 'ORD-'+Math.random().toString(36).slice(2,10)+'-'+Date.now();
    const rec = { id, created_at: now, payload: body };
    orders.unshift(rec);
    try { fs.writeFileSync(ordersFile, JSON.stringify(orders,null,2)); } catch(e){ console.warn('write /tmp failed',e); }
    return { status: 200, body: { ok:true, id } };
  } catch (err) {
    return { status: 500, body: { ok:false, error: String(err) } };
  }
};
JS

# Frontend: interactive 50/50 storefront page (Next.js route-ready)
mkdir -p apps/frontend/pages
cat > apps/frontend/pages/50-50.js <<'JSX'
import React from 'react'

const STORE = [
  { id:1, name:'Vintage Lamp', priceUsd:'12.99', priceEth:'0.0065', image:'/images/itemA.png', shipping:'Ships 3-5 days' },
  { id:2, name:'Handmade Wallet', priceUsd:'19.50', priceEth:'0.0098', image:'/images/itemB.png', shipping:'Ships 2-4 days' },
  { id:999, name:'Free 10 Models (special)', priceUsd:'19.99', priceEth:'0.00009', image:'/images/special.png', shipping:'Digital — pass Reese Truth Test', special:true }
];

export default function Store() {
  const handlePayPal = (price) => {
    // simple open to PayPal.me
    window.open('https://www.paypal.me/ReeseComp/'+price, '_blank');
  };
  const handleMetaMask = async (item) => {
    if(!window.ethereum){ alert('Install MetaMask'); return; }
    const provider = new window.ethers.providers.Web3Provider(window.ethereum);
    const s = provider.getSigner();
    const tx = await s.sendTransaction({ to: process.env.NEXT_PUBLIC_MERCHANT_ADDR || '0xc22f0db6ba49...', value: window.ethers.utils.parseEther(item.priceEth) });
    alert('TX sent: '+tx.hash);
    // call serverless orders endpoint to monitor/process
    await fetch('/api/orders', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ txHash: tx.hash, productId: item.id, priceEth: item.priceEth })});
  };

  return <div style={{padding:20, fontFamily:'system-ui'}}>
    <h1>Keystone 50/50 Store</h1>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))',gap:16}}>
      {STORE.map(it=>(
        <div key={it.id} style={{padding:12, borderRadius:12, boxShadow:'0 8px 30px rgba(2,6,23,.08)', background:'#fff'}}>
          <img src={it.image} style={{width:160,height:160,objectFit:'contain'}}/>
          <h3>{it.name}</h3>
          <div style={{fontWeight:800}}>${it.priceUsd} • {it.priceEth} ETH</div>
          <div style={{color:'#6b7280'}}>{it.shipping}</div>
          <div style={{marginTop:10,display:'flex',gap:8}}>
            <button onClick={()=>handleMetaMask(it)} style={{background:'#ffb347',border:0,padding:8,borderRadius:8}}>Buy ETH</button>
            <button onClick={()=>handlePayPal(it.priceUsd)} style={{background:'#0070ba',border:0,padding:8,borderRadius:8,color:'#fff'}}>PayPal</button>
          </div>
        </div>
      ))}
    </div>
  </div>
}
JSX

# Admin UI skeleton
mkdir -p admin
cat > admin/README.md <<'MD'
Admin console placeholder:
- Manage orders -> /api/orders (serverless returns /tmp list)
- Approve shipments, refund, revoke licenses
MD

# models + Shadow X helper
mkdir -p models
cat > models/README.md <<'MD'
Shadow X model sync helper
- Place model export (weights + tokenizer) in models/shadowx_export/
- Run: bash sync_shadowx_to_trinity.sh to prepare and push to Trinity/REPO
MD
cat > models/sync_shadowx_to_trinity.sh <<'SH'
#!/usr/bin/env bash
set -euo pipefail
echo "Sync helper: copy export files to Trinity models folder"
# edit the TRINITY_MODELS_DIR to where Trinity expects models
TRINITY_MODELS_DIR="${HOME}/Trinity/models"
SRC="$(pwd)/shadowx_export"
if [ ! -d "$SRC" ]; then
  echo "No export found at $SRC - please place Shadow X export there (weights + config)"
  exit 1
fi
mkdir -p "$TRINITY_MODELS_DIR"
cp -a "$SRC"/* "$TRINITY_MODELS_DIR"/
echo "Copied Shadow X export to $TRINITY_MODELS_DIR. Restart Trinity / ReeseOS services as needed."
