// This is your test publishable API key.
const stripe = Stripe("pk_test_51OuDSSP1CjHWdbKHXypRdLwCfdzz6jpGGPv3CPL0o7Thx4tSeUIruxMJvSIId5PURvjUQll0ljwV5dkLXSpJFG1R00rTqu7AJa");

initialize();

// Create a Checkout Session as soon as the page loads
async function initialize() {
  const response = await fetch("https://8000-petergarvan-horizonmark-ofungvqkje6.ws-eu110.gitpod.io/create-checkout-session/");

  const { clientSecret } = await response.json();

  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}