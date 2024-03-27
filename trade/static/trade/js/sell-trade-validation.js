// Collecting and processing data from the backend
const mydataElement = document.getElementById('open-trades');
const mytradeData = mydataElement.getAttribute('data');
const mymodifiedTradeData = mytradeData.replace(/'/g, '"');
const myOpenTrades = JSON.parse(mymodifiedTradeData);

// Getting the element to change 
const symbol = document.getElementById('symbol');
const quantityElement = document.getElementById('quantity');
const sellRadioButton = document.getElementById('sell');

// Add an event listener to the radio buttons
document.querySelectorAll('input[name="side"]').forEach(radioButton => {
    radioButton.addEventListener('change', () => {
        
        // Check if the "sell" button is selected
        if (sellRadioButton.checked) {
            let symbolQuantityDict = {};
            
            for (let trade of myOpenTrades) {
                const quantity = parseFloat(trade.quantity);
                
                // Check if the symbol already exists in the dictionary
                if (trade.symbol in symbolQuantityDict) {
                    symbolQuantityDict[trade.symbol] += quantity;
                } else {
                    symbolQuantityDict[trade.symbol] = quantity;
                }
            }
            
            // Set the max attribute to the value
            symbol.addEventListener('change', function() {
                if (symbol.value.toUpperCase() in symbolQuantityDict) {
                    quantityElement.max = symbolQuantityDict[symbol.value.toUpperCase()];
                }
            });
        }
    });
});