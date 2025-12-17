import React from 'react'

const STORE = [
  { id:1, name:'Vintage Lamp', priceUsd:'12.99', priceEth:'0.0065', image:'/images/itemA.png', shipping:'Ships 3-5 days' },
  { id:2, name:'Handmade Wallet', priceUsd:'19.50', priceEth:'0.0098', image:'/images/itemB.png', shipping:'Ships 2-4 days' },
  { id:999, name:'Free 10 Models (special)', priceUsd:'19.99', priceEth:'0.00009', image:'/images/special.png', shipping:'Digital — pass Reese Truth Test', special:true }
];

export default function Store() {
  const handlePayPal = (price) => {
    // simple open to PayPal.me
    window.open('https://www.paypal.me/ReeseComp/'+price, '_blank');
  };
  const handleMetaMask = async (item) => {
    if(!window.ethereum){ alert('Install MetaMask'); return; }
    const provider = new window.ethers.providers.Web3Provider(window.ethereum);
    const s = provider.getSigner();
    const tx = await s.sendTransaction({ to: process.env.NEXT_PUBLIC_MERCHANT_ADDR || '0xc22f0db6ba49...', value: window.ethers.utils.parseEther(item.priceEth) });
    alert('TX sent: '+tx.hash);
    // call serverless orders endpoint to monitor/process
    await fetch('/api/orders', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ txHash: tx.hash, productId: item.id, priceEth: item.priceEth })});
  };

  return <div style={{padding:20, fontFamily:'system-ui'}}>
    <h1>Keystone 50/50 Store</h1>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))',gap:16}}>
      {STORE.map(it=>(
        <div key={it.id} style={{padding:12, borderRadius:12, boxShadow:'0 8px 30px rgba(2,6,23,.08)', background:'#fff'}}>
          <img src={it.image} style={{width:160,height:160,objectFit:'contain'}}/>
          <h3>{it.name}</h3>
          <div style={{fontWeight:800}}>${it.priceUsd} • {it.priceEth} ETH</div>
          <div style={{color:'#6b7280'}}>{it.shipping}</div>
          <div style={{marginTop:10,display:'flex',gap:8}}>
            <button onClick={()=>handleMetaMask(it)} style={{background:'#ffb347',border:0,padding:8,borderRadius:8}}>Buy ETH</button>
            <button onClick={()=>handlePayPal(it.priceUsd)} style={{background:'#0070ba',border:0,padding:8,borderRadius:8,color:'#fff'}}>PayPal</button>
          </div>
        </div>
      ))}
    </div>
  </div>
}
