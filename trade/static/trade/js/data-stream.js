// Collecting and processing data from the backend
const dataElement = document.getElementById('open-trades');
const tradeData = dataElement.getAttribute('data');
const modifiedTradeData = tradeData.replace(/'/g, '"');
const openTrades = JSON.parse(modifiedTradeData);

console.log(openTrades);

// Connecting to Binance Websocket
const websocketEndpoint = 'wss://stream.binance.com:9443/ws';

// Keep Track of time, incase of need to throtte
let lastUpdateTimestamp = 0;

// Function to subscribe to the WebSocket stream
const subscribeToTicker = (id, symbol, side, quantity, entry, takeProfit, stopLoss) => {
    const ws = new WebSocket(websocketEndpoint);

    // Subscribing to the ticker stream
    ws.onopen = () => {
        const streamName = `${symbol.toLowerCase()}@ticker`;
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
                if (tickerData.c >= takeProfit || tickerData.c <= stopLoss) {
                    let form = document.getElementById(`form_${id}`);
                    form.submit()

                    removeTrade = openTrades.findIndex(trade => trade.id === id);
                    openTrades.splice(removeTrade, 1);
                }

                else {
                    const netElement = document.getElementById(id);
                    const netPosition = (parseFloat(tickerData.c) - parseFloat(entry)) * parseFloat(quantity);

                    if (side === 'BUY') {
                        netElement.style.color = (netPosition >= 0) ? "#11a452" : "#ef415b";
                    } else {
                        netElement.style.color = (netPosition > 0) ? "#ef415b" : "#11a452";
                        netPosition *= -1
                    }
                    netElement.innerHTML = netPosition.toFixed(2);
                    lastUpdateTimestamp = currentTime;
                }
            }
        }
    };

    // Handling errors
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};

openTrades.forEach(trade => {
    subscribeToTicker(
        trade.id,
        trade.symbol,
        trade.side,
        trade.quantity,
        trade.entry,
        trade.take_profit,
        trade.stop_loss
    );
});