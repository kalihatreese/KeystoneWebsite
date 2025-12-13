const { ethers } = require("ethers");
const fs = require("fs");
const crypto = require("crypto");

const INVOICE_FILE = "./invoices.json";

function load() {
  if (!fs.existsSync(INVOICE_FILE)) return [];
  return JSON.parse(fs.readFileSync(INVOICE_FILE));
}

function save(data) {
  fs.writeFileSync(INVOICE_FILE, JSON.stringify(data, null, 2));
}

function createInvoice(amountEth) {
  const wallet = ethers.Wallet.createRandom();

  return {
    id: crypto.randomUUID(),
    amount: amountEth,
    address: wallet.address,
    privateKey: wallet.privateKey, // store securely later
    status: "pending",
    created: Date.now()
  };
}

// --- MACHINE MODE ---
let invoices = load();
const invoice = createInvoice(0.05); // example

invoices.push(invoice);
save(invoices);

console.log("📄 MACHINE INVOICE CREATED");
console.log(invoice);
