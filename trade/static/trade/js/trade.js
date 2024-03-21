document.addEventListener("DOMContentLoaded", function() {
    const limitRadio = document.getElementById("limit");
    const marketRadio = document.getElementById("market");

    const limitInputsDiv = document.getElementById("limit-inputs");
    const priceInput = `
        <label for="price" class="withdrawal-label">Price</label>
        <input type="number" class="withdraw-input" name="price" required>
    `;

    function updateLimitInputs() {
        if (limitRadio.checked) {
            limitInputsDiv.innerHTML = priceInput;
        } 
        if (marketRadio.checked) {
            limitInputsDiv.innerHTML = '';
        }
    }

    // Initial check on page load
    updateLimitInputs();

    // Event listener for radio button change
    limitRadio.addEventListener("change", updateLimitInputs);
    marketRadio.addEventListener("change", updateLimitInputs);
});