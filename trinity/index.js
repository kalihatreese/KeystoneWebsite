require('dotenv').config();

const express = require('express');
const path = require('path');

const app = express();

/* ---------- Middleware ---------- */
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* ---------- Static UI ---------- */
app.use(express.static(path.join(__dirname, 'public')));

/* ---------- Health Check ---------- */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'Trinity', time: Date.now() });
});

/* ---------- Root ---------- */
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

/* ---------- Port ---------- */
const PORT = process.env.PORT || 3001;

/* ---------- Listen (ONCE) ---------- */
app.listen(PORT, '0.0.0.0', () => {
  console.log(`[Veritas] Trinity UI live on http://127.0.0.1:${PORT}`);
});
