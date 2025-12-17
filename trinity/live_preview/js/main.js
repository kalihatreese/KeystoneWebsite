document.querySelectorAll('.paypal-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.id;
    if(id) window.location.href = `https://www.paypal.com/checkoutnow?hosted_button_id=${id}`;
  });
});
document.querySelectorAll('.stripe-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    alert('Stripe integration coming soon');
  });
});
