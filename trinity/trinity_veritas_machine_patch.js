const fs = require("fs");
const LOG_FILE = "./veritas_log.txt";
const INVOICE_FILE = "./invoices.json";

function veritasLog(message) {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(LOG_FILE, `[${timestamp}] ${message}\n`);
  console.log(`[Veritas] ${message}`);
}

function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  return JSON.parse(fs.readFileSync(INVOICE_FILE));
}

function saveInvoices(invoices) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(invoices, null, 2));
}

function processPayments() {
  const invoices = loadInvoices();
  if (!invoices.length) return;

  invoices.forEach(invoice => {
    if (invoice.status === "pending") {
      invoice.status = "paid";
      const client = invoice.intent?.client || "UNKNOWN";
      const property = invoice.intent?.propertyID || "UNKNOWN";
      veritasLog(`Payment received for invoice ${invoice.id} (${invoice.amount} ETH). Client: ${client}, Property: ${property}`);
    }
  });

  saveInvoices(invoices);
}

// Run the machine
veritasLog("⚙️ Trinity + Veritas Machine PATCH ONLINE");
processPayments();
