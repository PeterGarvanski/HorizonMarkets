// Get a reference to the symbol element
const symbol = document.getElementById('symbol');

// Add an onchange event listener to it
symbol.addEventListener('change', function() {
    const websocketEndpoint = 'wss://stream.binance.com:9443/ws';
    
    // Keep Track of time, incase of need to throtte
    let lastUpdateTimestamp = 0;
    
    // Function to subscribe to the WebSocket stream
    const subscribeToTicker = (ticker) => {
        const ws = new WebSocket(websocketEndpoint);
    
        // Subscribing to the ticker stream
        ws.onopen = () => {
            const streamName = `${ticker.toLowerCase()}@ticker`;
            const subscriptionMsg = JSON.stringify({
                method: 'SUBSCRIBE',
                params: [streamName],
                id: 1
            });
            ws.send(subscriptionMsg);
        };
    
        // Handling incoming data, and updating Elements
        ws.onmessage = (event) => {
            const currentTime = Date.now();
            if (currentTime - lastUpdateTimestamp >= 0) {
                const tickerData = JSON.parse(event.data);
                
                if (tickerData.e === '24hrTicker') {
                    const quantityElement = document.getElementById('quantity');
                    const accountBalanceElement = document.getElementById('account-balance');
                    const accountBalance = accountBalanceElement.getAttribute('data');
                    const maxQuantity = (parseFloat(accountBalance) - 100) / parseFloat(tickerData.c);
    
                    quantityElement.max = maxQuantity;
                    lastUpdateTimestamp = currentTime;

                    ws.close();
                }
            }
        };
    
        // Handling errors
        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    };
    
    subscribeToTicker(symbol.value)
});