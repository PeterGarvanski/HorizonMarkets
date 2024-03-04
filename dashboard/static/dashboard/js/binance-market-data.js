// Collecting and processing data from the backend
const dataElement = document.getElementsByClassName('fav-tickers')[0];
const cryptoList = dataElement.getAttribute('data');
const modifiedCryptoList = cryptoList.replace(/'/g, '"');
const favTickers = JSON.parse(modifiedCryptoList);

// Connecting to Binance Websocket
const websocketEndpoint = 'wss://stream.binance.com:9443/ws';
const ws = new WebSocket(websocketEndpoint);

// Keep Track of time, incase of need to throtte
let lastUpdateTimestamp = 0;

// Function to subscribe to the WebSocket stream
const subscribeToTicker = (ticker) => {
    const ws = new WebSocket(websocketEndpoint); // Create a new WebSocket connection

    // Subscribing to the ticker stream
    ws.onopen = () => {
        const streamName = `${ticker.toLowerCase()}usdt@ticker`;
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
                const tickerValueElement = document.getElementById(`${tickerData.s}_value`);
                const tickerPercentageElement = document.getElementById(`${tickerData.s}_percentage`);

                const tickerPrice = parseFloat(tickerData.c);
                const tickerPercentage = parseFloat(tickerData.P);

                if (tickerPercentage > 0) {
                    tickerPercentageElement.style.backgroundColor = "#11a452";
                    
                } else if (tickerPercentage < 0) {
                    tickerPercentageElement.style.backgroundColor = "#ef415b";

                } else {
                    tickerPercentageElement.style.backgroundColor = "#93b8e1";
                }

                tickerValueElement.innerHTML = tickerPrice.toFixed(2);
                tickerPercentageElement.innerHTML = tickerPercentage.toFixed(2) + "%";

                lastUpdateTimestamp = currentTime;
            }
        }
    };

    // Handling errors
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};

// Function to subscribe to tickers using multiple WebSocket connections
const subscribeToTickers = (tickers) => {
    tickers.forEach(ticker => {
        subscribeToTicker(ticker);
    });
};

// Calling the function to subscribe to ticker streams
subscribeToTickers(favTickers);