#!/bin/bash

echo "🛑 Stopping any running injectors..."
pkill -f inject_invoices || true
pkill -f inject_invoices_loop || true

echo "🧠 Finalizing Trinity build..."

cat << 'JS' > dashboard.js
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send(`
    <html>
    <head>
      <title>Trinity Dashboard</title>
      <style>
        body { background:#0e0e0e; color:#00ffcc; font-family: monospace; padding:20px; }
        h1 { color:#ffffff; }
        pre { background:#111; padding:15px; border-radius:8px; }
      </style>
    </head>
    <body>
      <h1>🧿 Trinity Multi‑Chain Server</h1>
      <p>Status: LIVE</p>
      <pre id="data">Loading invoices...</pre>
      <script>
        async function load() {
          const r = await fetch('/api/invoices');
          const d = await r.json();
          document.getElementById('data').textContent =
            JSON.stringify(d, null, 2);
        }
        load();
        setInterval(load, 3000);
      </script>
    </body>
    </html>
  `);
});

module.exports = app;
JS

echo "🔌 Wiring dashboard into server..."

sed -i '/app.use(express.json())/a \
const dashboard = require("./dashboard");\napp.use("/", dashboard);\n' index.js

echo "🚀 Restarting Trinity server..."
pkill -f index.js || true
node index.js &

sleep 2

echo "🌍 Starting Serveo public tunnel..."
ssh -R 80:localhost:3001 serveo.net &

echo ""
echo "✅ BUILD COMPLETE"
echo "📡 Local API:    http://localhost:3001"
echo "🌐 Public URL:  https://$(whoami).serveo.net"
echo "📊 Dashboard:   /"
echo ""
echo "🧱 Trinity is LIVE."
