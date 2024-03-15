// This is your test publishable API key.
const stripe = Stripe("pk_test_51OuDSSP1CjHWdbKHXypRdLwCfdzz6jpGGPv3CPL0o7Thx4tSeUIruxMJvSIId5PURvjUQll0ljwV5dkLXSpJFG1R00rTqu7AJa");
response = {"clientSecret": "cs_test_a1BIHCmBqdwuxjByUDl4985vYTTe5p5TOH2oPaggUtd69Tcw9f4SjOWCiq_secret_fidwbEhqYWAnPydgaGdgYWFgYScpJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ3dgYWx3YGZxSmtGamh1aWBxbGprJz8nZGlyZHx2JyknZ2RmbmJ3anBrYUZqaWp3Jz8nJmNjY2NjYyd4JSUl"}

const { clientSecret } = response;

initialize();

// Create a Checkout Session as soon as the page loads
async function initialize() {
  const checkout = await stripe.initEmbeddedCheckout({
    clientSecret,
  });

  // Mount Checkout
  checkout.mount('#checkout');
}