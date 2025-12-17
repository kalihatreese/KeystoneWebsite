require('dotenv').config();
const axios = require('axios');

const INFURA_URL = `https://mainnet.infura.io/v3/${process.env.INFURA_KEY}`;

// Fetch latest block number
async function getLatestBlock() {
  try {
    const response = await axios.post(
      INFURA_URL,
      {
        jsonrpc: "2.0",
        method: "eth_blockNumber",
        params: [],
        id: 1
      },
      { headers: { "Content-Type": "application/json" } }
    );
    return parseInt(response.data.result, 16); // convert hex to decimal
  } catch (err) {
    console.error("Infura Error:", err.message);
    return null;
  }
}

// Example usage
(async () => {
  const block = await getLatestBlock();
  console.log("Latest Ethereum block:", block);
})();

module.exports = { getLatestBlock };
