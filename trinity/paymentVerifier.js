require('dotenv').config();
const { ethers } = require('ethers');
const TronWebImport = require('tronweb');
const TronWeb = TronWebImport.default || TronWebImport;

// Providers
const ethProvider = new ethers.JsonRpcProvider(process.env.ETH_RPC);
const polygonProvider = new ethers.JsonRpcProvider(process.env.POLYGON_RPC);
const tronWeb = new TronWeb({ fullHost: process.env.TRON_RPC });

// Track pending invoices
let pendingInvoices = [];

// Add invoices to watch
function watchInvoice(invoice) {
    pendingInvoices.push(invoice);
}

// Check ETH/Polygon payments
async function checkEVMPayments() {
    for (const invoice of pendingInvoices) {
        if (invoice.status !== 'pending') continue;
        const provider = invoice.chain === 'polygon' ? polygonProvider : ethProvider;
        try {
            const balance = await provider.getBalance(invoice.wallet);
            const formattedBalance = parseFloat(ethers.formatEther(balance));
            if (formattedBalance >= parseFloat(invoice.amount)) {
                invoice.status = 'paid';
                console.log(`Invoice ${invoice.invoiceId} PAID on ${invoice.chain}`);
            }
        } catch(e) {
            console.error(`Error checking ${invoice.chain} for ${invoice.wallet}:`, e.message);
        }
    }
}

// Check TRX payments
async function checkTronPayments() {
    for (const invoice of pendingInvoices) {
        if (invoice.status !== 'pending' || invoice.chain !== 'tron') continue;
        try {
            const balance = await tronWeb.trx.getBalance(invoice.wallet);
            const formattedBalance = balance / 1_000_000; // TRX has 6 decimals
            if (formattedBalance >= parseFloat(invoice.amount)) {
                invoice.status = 'paid';
                console.log(`Invoice ${invoice.invoiceId} PAID on TRX`);
            }
        } catch(e) {
            console.error(`Error checking TRX for ${invoice.wallet}:`, e.message);
        }
    }
}

// Run every 15 seconds
setInterval(() => {
    checkEVMPayments();
    checkTronPayments();
}, 15000);

module.exports = { watchInvoice, pendingInvoices };
function logPayment(invoice) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] Payment confirmed: ${invoice.invoiceId} | ${invoice.chain} | ${invoice.wallet} | ${invoice.amount}`);
}
const originalCheckEVMPayments = checkEVMPayments;
checkEVMPayments = async () => {
    await originalCheckEVMPayments();
    pendingInvoices.filter(inv => inv.status==='paid').forEach(logPayment);
};
const originalCheckTronPayments = checkTronPayments;
checkTronPayments = async () => {
    await originalCheckTronPayments();
    pendingInvoices.filter(inv => inv.status==='paid').forEach(logPayment);
};
