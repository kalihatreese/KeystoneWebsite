const { ethers } = require("ethers");
const fs = require("fs");
const crypto = require("crypto");

const INVOICE_FILE = "./invoices.json";
const LOG_FILE = "./veritas_log.txt";

function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  return JSON.parse(fs.readFileSync(INVOICE_FILE));
}

function saveInvoices(invoices) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(invoices, null, 2));
}

function veritasLog(message) {
  const timestamp = new Date().toISOString();
  fs.appendFileSync(LOG_FILE, `[${timestamp}] ${message}\n`);
  console.log(`[Veritas] ${message}`);
}

function createInvoice(amountEth, client, propertyID, serviceType) {
  const wallet = ethers.Wallet.createRandom();
  const invoice = {
    id: crypto.randomUUID(),
    amount: amountEth,
    address: wallet.address,
    privateKey: wallet.privateKey,
    status: "pending",
    created: Date.now(),
    intent: {
      client,
      propertyID,
      serviceType
    }
  };
  veritasLog(`Invoice created for client ${client}, property ${propertyID}, service ${serviceType}, amount ${amountEth} ETH`);
  return invoice;
}

function processPayments() {
  const invoices = loadInvoices();
  if (!invoices.length) return;

  invoices.forEach(invoice => {
    if (invoice.status === "pending") {
      invoice.status = "paid";
      veritasLog(`Payment received for invoice ${invoice.id} (${invoice.amount} ETH). Client: ${invoice.intent.client}, Property: ${invoice.intent.propertyID}`);
    }
  });

  saveInvoices(invoices);
}

console.log("⚙️  Trinity + Veritas Machine ONLINE");

const invoices = loadInvoices();
const newInvoice = createInvoice(0.05, "John Doe", "PROP-1001", "Consultation");
invoices.push(newInvoice);
saveInvoices(invoices);

processPayments();
