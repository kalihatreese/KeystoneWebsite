const { ethers } = require('ethers');
function isValidWallet(address, chain = 'eth') {
    if(chain === 'tron') return /^T[a-zA-Z0-9]{33}$/.test(address);
    try { return ethers.isAddress(address); } catch { return false; }
}
module.exports = { isValidWallet };
