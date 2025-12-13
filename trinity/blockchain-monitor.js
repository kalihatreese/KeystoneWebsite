require('dotenv').config(); 
const Web3 = require('web3'); 
const ws = new Web3(new Web3.providers.WebsocketProvider(`wss://mainnet.infura.io/ws/v3/${process.env.INFURA_KEY}`)); 
const { line, table, screen } = require('./trinity-dashboard'); 

const WHALE_THRESHOLD_ETH = 100; 
const TOKEN_CONTRACTS = ['0x6B175474E89094C44Da98b954EedeAC495271d0F','0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48']; // DAI & USDC as example

async function analyzeBlock(blockNumber){
    const block = await ws.eth.getBlock(blockNumber,true); 
    const highValueTxs = [];
    block.transactions.forEach(tx => {
        const valueEth = Web3.utils.fromWei(tx.value,'ether');
        if(Number(valueEth) >= WHALE_THRESHOLD_ETH){
            highValueTxs.push([tx.hash, valueEth, tx.from, tx.to]);
        }
        TOKEN_CONTRACTS.forEach(addr=>{
            if(tx.to && tx.to.toLowerCase()===addr.toLowerCase()){ 
                console.log(`Token interaction: ${tx.hash} -> ${addr}`); 
            }
        });
    });
    if(highValueTxs.length>0){
        console.log(`High-value transactions in block ${blockNumber}:`, highValueTxs);
        table.setData({headers:['TxHash','Value','From','To'],data:highValueTxs});
        screen.render();
    }
}

ws.eth.subscribe('newBlockHeaders',(err,block)=>{
    if(!err){
        console.log(`New block #${block.number}`); 
        analyzeBlock(block.number);
        line.setData([{title:'Blocks',x:[block.number],y:[block.transactions.length]}]);
        screen.render();
    }
});

// --- Optional MEV / Arbitrage detector ---
ws.eth.subscribe('pendingTransactions', async (err, txHash)=>{
    if(!err){
        try{
            const tx = await ws.eth.getTransaction(txHash);
            if(tx && tx.value && Number(Web3.utils.fromWei(tx.value,'ether'))>50){ 
                console.log(`Pending high-value tx detected: ${tx.hash}`); 
            }
        }catch(e){/* ignore errors */}
    }
});

