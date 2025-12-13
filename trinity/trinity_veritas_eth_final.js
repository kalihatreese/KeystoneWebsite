require('dotenv').config();
const { ethers } = require("ethers");
const fs = require("fs");

const RPC = process.env.ETH_RPC || "https://rpc.ankr.com/eth";
const provider = new ethers.JsonRpcProvider(RPC);

const INVOICE_FILE = "./invoices.json";
const LOG_FILE = "./veritas.log";

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`;
  fs.appendFileSync(LOG_FILE, line);
  console.log("[Veritas]", msg);
}

function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  return JSON.parse(fs.readFileSync(INVOICE_FILE));
}

function saveInvoices(data) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(data, null, 2));
}

async function checkInvoice(invoice) {
  try {
    const balance = await provider.getBalance(invoice.address);
    const eth = Number(ethers.formatEther(balance));

    if (eth >= invoice.amount) {
      invoice.status = "paid";
      invoice.paidAt = Date.now();
      log(`💰 PAYMENT CONFIRMED | ${invoice.amount} ETH | ${invoice.address}`);
      log(`Client: ${invoice.intent?.client || "AUTO"} | Property: ${invoice.intent?.propertyID || "AUTO"}`);
    }
  } catch (e) {
    log(`⚠️ RPC issue — retrying next cycle`);
  }
}

async function cycle() {
  const invoices = loadInvoices();
  let dirty = false;

  for (const invoice of invoices) {
    if (invoice.status !== "pending") continue;
    await checkInvoice(invoice);
    dirty = true;
  }

  if (dirty) saveInvoices(invoices);
}

log("⚙️ VERITAS ETH PAYMENT MACHINE LIVE");

setInterval(cycle, 15000);
