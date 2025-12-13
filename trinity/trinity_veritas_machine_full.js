const fs = require("fs");
const path = require("path");

const INVOICE_FILE = path.join(__dirname, "invoices.json");
const LOG_FILE = path.join(__dirname, "veritas_log.txt");

// Utility to log Veritas messages
function veritasLog(message) {
  const timestamp = new Date().toISOString();
  console.log(`[Veritas] ${message}`);
  fs.appendFileSync(LOG_FILE, `[${timestamp}] ${message}\n`);
}

// Load invoices
function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  return JSON.parse(fs.readFileSync(INVOICE_FILE));
}

// Save invoices
function saveInvoices(invoices) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(invoices, null, 2));
}

// Fill missing metadata
function fillInvoiceMetadata(invoice) {
  if (!invoice.intent) invoice.intent = {};
  if (!invoice.intent.client) invoice.intent.client = "UNKNOWN";
  if (!invoice.intent.propertyID) invoice.intent.propertyID = "UNKNOWN";
  return invoice;
}

// Process pending payments
function processPayments() {
  const invoices = loadInvoices();
  let updated = false;

  invoices.forEach((invoice) => {
    fillInvoiceMetadata(invoice);

    if (invoice.status === "pending") {
      invoice.status = "paid";
      veritasLog(`Payment received for invoice ${invoice.id} (${invoice.amount} ETH). Client: ${invoice.intent.client}, Property: ${invoice.intent.propertyID}`);
      updated = true;
    }
  });

  if (updated) saveInvoices(invoices);
}

// Continuous monitoring
veritasLog("⚙️ Trinity + Veritas Machine FULL PATCH ONLINE");

setInterval(() => {
  processPayments();
}, 5000); // check every 5 seconds

// Initial run
processPayments();
