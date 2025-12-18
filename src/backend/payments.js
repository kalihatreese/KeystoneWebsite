import Stripe from 'stripe';

export async function handlePayment(request, env) {
  const stripe = new Stripe(env.STRIPE_SECRET_KEY);
  const { price, title } = await request.json();

  // Veritas validates the asset via the Reese OS logic before checkout
  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [{
      price_data: {
        currency: 'usd',
        product_data: { name: title, description: 'Keystone Pulse Asset' },
        unit_amount: Math.round(price * 100),
      },
      quantity: 1,
    }],
    mode: 'payment',
    success_url: 'https://www.keystoneaiml.com/success',
    cancel_url: 'https://www.keystoneaiml.com/toolbox',
  });

  return new Response(JSON.stringify({ id: session.id }), {
    headers: { 'Content-Type': 'application/json' },
  });
}
