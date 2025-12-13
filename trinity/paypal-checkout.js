const paypal = require('@paypal/checkout-server-sdk');
require('dotenv').config();

const environment = new paypal.core.LiveEnvironment(
process.env.PAYPAL_CLIENT_ID,
process.env.PAYPAL_SECRET
);
const client = new paypal.core.PayPalHttpClient(environment);

async function createOrder(amount = "50.00", currency = "USD") {
const request = new paypal.orders.OrdersCreateRequest();
request.prefer("return=representation");
request.requestBody({
intent: "CAPTURE",
purchase_units: [{ amount: { currency_code: currency, value: amount } }]
});
const order = await client.execute(request);
return order.result;
}

async function captureOrder(orderId) {
const request = new paypal.orders.OrdersCaptureRequest(orderId);
request.requestBody({});
const capture = await client.execute(request);
return capture.result;
}

module.exports = { createOrder, captureOrder };
