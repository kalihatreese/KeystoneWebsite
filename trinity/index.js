const express = require("express");
const fs = require("fs");
const crypto = require("crypto");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3001;
const INVOICE_FILE = "./invoices.json";

app.use(express.json());
const dashboard = require("./dashboard");
app.use("/", dashboard);

app.use(express.static(path.join(__dirname, "public")));

function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(INVOICE_FILE));
  } catch (error) {
    console.error("Error reading or parsing invoices.json:", error.message);
    return [];
  }
}

function saveInvoices(data) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(data, null, 2));
}

app.post("/api/machine/invoice", (req, res) => {
  const { amount, client, propertyID } = req.body || {};

  // Basic input validation/check
  if (typeof amount !== 'number' || amount <= 0) {
    return res.status(400).json({ error: "Invalid or missing 'amount' field." });
  }
  if (!client || !propertyID) {
    return res.status(400).json({ error: "Missing 'client' or 'propertyID' field." });
  }

  const invoice = {
    id: crypto.randomUUID(),
    amount: amount,
    status: "pending",
    created: Date.now(),
    intent: {
      client: client,
      propertyID: propertyID,
      role: "Veritas Escort"
    }
  };

  const invoices = loadInvoices();
  invoices.push(invoice);
  saveInvoices(invoices);

  console.log("[Veritas] Invoice created:", invoice);
  res.json(invoice);
});

// Start the server
app.listen(PORT, "0.0.0.0", () => {
  console.log(`[Veritas] Trinity Payment Machine API listening on http://0.0.0.0:${PORT}`);
});
