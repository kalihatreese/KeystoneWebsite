# TRINITY CRYPTO RENTAL SYSTEM SETUP

# 1. Backend: Node.js API
# File: index.js
require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const ETH_WALLET = process.env.ETH_WALLET;
const POLYGON_WALLET = process.env.POLYGON_WALLET;
const TRX_WALLET = process.env.TRX_WALLET;

function createInvoice(wallet, amount, chain) {
  const invoice = {
    invoiceId: Math.random().toString(36).substr(2, 9),
    wallet,
    amount,
    chain,
    status: 'pending',
    message: `Send exactly ${amount} ${chain} to ${wallet}`
  };
  console.log('Invoice created:', invoice);
  return invoice;
}

app.post('/create-eth-invoice', (req, res) => {
  const { amount } = req.body;
  if (!amount) return res.status(400).json({ error: 'Amount required' });
  res.json(createInvoice(ETH_WALLET, amount, 'ETH'));
});

app.post('/create-polygon-invoice', (req, res) => {
  const { amount } = req.body;
  if (!amount) return res.status(400).json({ error: 'Amount required' });
  res.json(createInvoice(POLYGON_WALLET, amount, 'MATIC'));
});

app.post('/create-trx-invoice', (req, res) => {
  const { amount } = req.body;
  if (!amount) return res.status(400).json({ error: 'Amount required' });
  res.json(createInvoice(TRX_WALLET, amount, 'TRX'));
});

app.get('/health', (req, res) => res.json({ ok: true, service: 'trinity-payments' }));

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Trinity Crypto server running on port ${PORT}`));

# 2. Frontend: React Dashboard (TrinityDashboard.js)
import React, { useState } from 'react';

function TrinityDashboard() {
  const [amount, setAmount] = useState('');
  const [chain, setChain] = useState('ETH');
  const [invoice, setInvoice] = useState(null);

  async function createInvoice() {
    const endpoint = {
      ETH: 'create-eth-invoice',
      MATIC: 'create-polygon-invoice',
      TRX: 'create-trx-invoice'
    }[chain];

    const res = await fetch(`http://localhost:3001/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount })
    });
    const data = await res.json();
    setInvoice(data);
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Trinity Crypto Checkout</h1>
      <input
        type="number"
        placeholder="Amount"
        value={amount}
        onChange={e => setAmount(e.target.value)}
      />
      <select value={chain} onChange={e => setChain(e.target.value)}>
        <option value="ETH">ETH</option>
        <option value="MATIC">Polygon</option>
        <option value="TRX">TRX</option>
      </select>
      <button onClick={createInvoice}>Create Invoice</button>

      {invoice && (
        <div style={{ marginTop: 20 }}>
          <h2>Invoice Created</h2>
          <p><b>Invoice ID:</b> {invoice.invoiceId}</p>
          <p><b>Wallet:</b> {invoice.wallet}</p>
          <p><b>Amount:</b> {invoice.amount} {invoice.chain}</p>
          <p>{invoice.message}</p>
          <p><b>Status:</b> {invoice.status}</p>
        </div>
      )}
    </div>
  );
}

export default TrinityDashboard;

# 3. .env Example
ETH_WALLET=0xYourEthWalletAddress
POLYGON_WALLET=0xYourPolygonWalletAddress
TRX_WALLET=TYourTronWalletAddress
PORT=3001

# 4. Workflow
# 1. Customer opens dashboard
# 2. Selects chain (ETH / Polygon / TRX) and amount
# 3. Clicks “Create Invoice”
# 4. Invoice with wallet info and payment instructions is shown
# 5. After payment, backend can later check blockchain for confirmation
# 6. Access to Trinity hall/session is granted automatically

