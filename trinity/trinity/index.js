const express = require('express');
const { createOrder, captureOrder } = require('./paypal-checkout');
const blessed = require('blessed');
const contrib = require('blessed-contrib');
require('dotenv').config();

const app = express();
app.use(express.json());
const PORT = process.env.PORT || 3000;

// --- Dashboard ---
const screen = blessed.screen();
const grid = new contrib.grid({ rows: 12, cols: 12, screen: screen });
const line = grid.set(0, 0, 6, 12, contrib.line, {
label: 'Trinity Prices',
showLegend: true,
style: { line: 'green', text: 'white', baseline: 'black' }
});
const table = grid.set(6, 0, 6, 12, contrib.table, {
keys: true,
fg: 'white',
label: 'Positions',
columnSpacing: 2,
columnWidth: [10, 10, 10, 10]
});
setInterval(() => {
line.setData([{ title: 'Asset', x: ['T1','T2','T3'], y: [Math.random()*10, Math.random()*10, Math.random()*10] }]);
table.setData({ headers: ['Sym','Qty','Price','P/L'], data: [['AAPL','10','151','+1.5'],['TSLA','5','320','-2.0']] });
screen.render();
}, 1000);
screen.key(['escape','q','C-c'], () => process.exit(0));

// --- PayPal Routes ---
app.post('/create-order', async (req, res) => {
try {
const { amount } = req.body;
const order = await createOrder(amount || "50.00");
res.json(order);
} catch (err) {
console.error(err);
res.status(500).json({ error: err.message });
}
});

app.post('/capture-order', async (req, res) => {
try {
const { orderId } = req.body;
const capture = await captureOrder(orderId);
res.json(capture);
} catch (err) {
console.error(err);
res.status(500).json({ error: err.message });
}
});

// --- Start Server ---
app.listen(PORT, () => console.log("Trinity running on port ${PORT}"));

// --- Infura Module ---
const { getLatestBlock } = require('./infura');

// Live Ethereum Block Display
const blockLine = grid.set(0, 0, 2, 12, contrib.line, {
  label: 'Ethereum Latest Block',
  showLegend: true,
  style: { line: 'cyan', text: 'white', baseline: 'black' }
});

setInterval(async () => {
  const latestBlock = await getLatestBlock();
  blockLine.setData([
    { title: 'ETH', x: ['T1'], y: [latestBlock || 0] }
  ]);
  screen.render();
}, 5000); // update every 5 seconds
