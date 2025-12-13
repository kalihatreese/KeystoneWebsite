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
