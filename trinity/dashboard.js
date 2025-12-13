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
