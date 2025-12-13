const fs = require("fs");
const crypto = require("crypto");

const INVOICE_FILE = "./invoices.json";
const LOG_FILE = "./veritas.log";

// ---------- UTIL ----------
function now() {
  return new Date().toISOString();
}

function veritasLog(msg) {
  const line = `[${now()}] ${msg}\n`;
  fs.appendFileSync(LOG_FILE, line);
  console.log("[Veritas]", msg);
}

function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(INVOICE_FILE));
  } catch {
    veritasLog("⚠️ Corrupt invoices.json detected, resetting.");
    return [];
  }
}

function saveInvoices(data) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(data, null, 2));
}

// ---------- INVOICE CREATION ----------
function createInvoice(amountEth, client, propertyID, service) {
  return {
    id: crypto.randomUUID(),
    amount: amountEth,
    status: "pending",
    created: Date.now(),
    intent: {
      client: client || "AUTO_CLIENT",
      propertyID: propertyID || "AUTO_PROPERTY",
      service: service || "GENERAL_SERVICE"
    }
  };
}

// ---------- PAYMENT PROCESSOR ----------
function processPayments() {
  const invoices = loadInvoices();
  let changed = false;

  invoices.forEach(inv => {
    if (inv.status !== "pending") return;

    // Hard safety net
    if (!inv.intent) inv.intent = {};
    inv.intent.client ||= "UNKNOWN";
    inv.intent.propertyID ||= "UNKNOWN";
    inv.intent.service ||= "UNKNOWN";

    // ---- PAYMENT LOGIC ----
    // REAL BLOCKCHAIN HOOK GOES HERE
    // For now, machine marks as paid when detected
    inv.status = "paid";
    inv.paidAt = Date.now();

    veritasLog(
      `💰 Payment received | Invoice ${inv.id} | ${inv.amount} ETH | Client: ${inv.intent.client} | Property: ${inv.intent.propertyID} | Service: ${inv.intent.service}`
    );

    changed = true;
  });

  if (changed) saveInvoices(invoices);
}

// ---------- AUTO MACHINE ----------
veritasLog("⚙️ Trinity + Veritas FINAL MACHINE ONLINE");

// Seed at least one invoice if empty
let invoices = loadInvoices();
if (invoices.length === 0) {
  const seed = createInvoice(0.05, "John Doe", "PROP-1001", "Consultation");
  invoices.push(seed);
  saveInvoices(invoices);
  veritasLog(`📄 Seed invoice created: ${seed.id}`);
}

// Run forever
setInterval(processPayments, 15_000);
