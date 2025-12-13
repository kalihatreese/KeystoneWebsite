const { ethers } = require("ethers");
const fs = require("fs");
require("dotenv").config();

const RPC_URL = process.env.ETH_RPC;
const PROVIDER = new ethers.JsonRpcProvider(RPC_URL);
const INVOICE_FILE = "./invoices.json";
const CHECK_INTERVAL = 15000; // 15 seconds

function loadInvoices() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  return JSON.parse(fs.readFileSync(INVOICE_FILE));
}

function saveInvoices(invoices) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(invoices, null, 2));
}

console.log("⚙️  Trinity Payment Machine ONLINE (HTTP MODE)");

async function checkPayments() {
  const invoices = loadInvoices();
  if (!invoices.length) return;

  for (const invoice of invoices) {
    if (invoice.status !== "pending") continue;

    try {
      const balance = await PROVIDER.getBalance(invoice.address);
      const eth = parseFloat(ethers.formatEther(balance));

      if (eth >= invoice.amount) {
        invoice.status = "paid";
        invoice.paidAt = Date.now();

        console.log("💰 PAYMENT CONFIRMED");
        console.log(`Invoice: ${invoice.id}`);
        console.log(`Address: ${invoice.address}`);
        console.log(`Amount:  ${eth} ETH`);

        saveInvoices(invoices);
      }
    } catch (err) {
      console.error("RPC error:", err.message);
    }
  }
}

setInterval(checkPayments, CHECK_INTERVAL);
