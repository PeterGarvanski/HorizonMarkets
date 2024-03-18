const form = document.getElementById('deposit-form');
const input = document.getElementsByClassName('amount-multiplier')[0];

input.addEventListener('change', function(event) {
    form.submit();
});