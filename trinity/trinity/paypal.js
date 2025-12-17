const express=require('express');
const axios=require('axios');
require('dotenv').config();
const app=express();
app.use(express.json());

app.post('/create-paypal-order', async (req,res)=>{
  try{
    const order = await axios({
      url: "https://api-m.paypal.com/v2/checkout/orders",
      method: "post",
      auth:{
        username: process.env.PAYPAL_CLIENT_ID,
        password: process.env.PAYPAL_SECRET
      },
      data:{
        intent:"CAPTURE",
        purchase_units:[{ amount:{ currency_code:"USD", value:"99.00" } }]
      }
    });
    res.json({ id: order.data.id });
  }catch(e){
    console.error(e.response.data);
    res.status(500).send("paypal_error");
  }
});

app.listen(3001,()=>console.log("PayPal server on 3001"));
