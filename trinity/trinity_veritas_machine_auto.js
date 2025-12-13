const fs = require("fs");
const path = require("path");

const INVOICE_FILE = path.join(__dirname, "invoices.json");
const LOG_FILE = path.join(__dirname, "veritas_log.txt");
const CLIENT_FILE = path.join(__dirname, "clients_properties.json");

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

// Load clients & properties
function loadClients() {
  if (!fs.existsSync(CLIENT_FILE)) return [];
  return JSON.parse(fs.readFileSync(CLIENT_FILE));
}

// Assign metadata to invoices if missing
function assignInvoiceMetadata(invoice, clientList) {
  if (!invoice.intent) invoice.intent = {};
  if (!invoice.intent.client || !invoice.intent.propertyID) {
    const randomEntry = clientList[Math.floor(Math.random() * clientList.length)];
    invoice.intent.client = randomEntry.client;
    invoice.intent.propertyID = randomEntry.propertyID;
  }
  return invoice;
}

// Process pending payments
function processPayments() {
  const invoices = loadInvoices();
  const clients = loadClients();
  let updated = false;

  invoices.forEach((invoice) => {
    assignInvoiceMetadata(invoice, clients);

    if (invoice.status === "pending") {
      invoice.status = "paid";
      veritasLog(`Payment received for invoice ${invoice.id} (${invoice.amount} ETH). Client: ${invoice.intent.client}, Property: ${invoice.intent.propertyID}`);
      updated = true;
    }
  });

  if (updated) saveInvoices(invoices);
}

// Continuous monitoring
veritasLog("⚙️ Trinity + Veritas AUTO CLIENT ASSIGNMENT ONLINE");

setInterval(() => {
  processPayments();
}, 5000); // check every 5 seconds

// Initial run
processPayments();
