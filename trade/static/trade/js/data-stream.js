// Collecting and processing data from the backend
const dataElement = document.getElementById('open-trades');
const tradeData = dataElement.getAttribute('data');
const modifiedTradeData = tradeData.replace(/'/g, '"');
const openTrades = JSON.parse(modifiedTradeData);

// Connecting to Binance Websocket
const websocketEndpoint = 'wss://stream.binance.com:9443/ws';
const ws = new WebSocket(websocketEndpoint);

// Keep Track of time, incase of need to throtte
let lastUpdateTimestamp = 0;

// Function to subscribe to the WebSocket stream
const subscribeToTicker = (ticker, id, entry) => {
    const ws = new WebSocket(websocketEndpoint); // Create a new WebSocket connection

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
                const netElement = document.getElementById(id);
                const netPosition = parseFloat(tickerData.c) - parseFloat(entry);

                if (netPosition >= 0) {
                    netElement.style.color = "#11a452";
                    
                } else {
                    netElement.style.color = "#ef415b";
                }

                netElement.innerHTML = `$${netPosition.toFixed(2)}`;
                lastUpdateTimestamp = currentTime;
            }
        }
    };

    // Handling errors
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};

openTrades.forEach(trade => {
    subscribeToTicker(trade.symbol, trade.id, trade.entry)
});