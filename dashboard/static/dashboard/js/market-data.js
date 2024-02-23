// The WebSocket endpoint for Coinbase's WebSocket feed
const websocketEndpoint = 'wss://ws-feed.pro.coinbase.com';

// Collecting and processing data from the backend
const dataElement = document.getElementsByClassName('fav-tickers')[0];
const cryptoList = dataElement.getAttribute('data');
const modifiedCryptoList = cryptoList.replace(/'/g, '"');
const favTickers = JSON.parse(modifiedCryptoList);


// Create a WebSocket connection
const ws = new WebSocket(websocketEndpoint);

// Open WebSocket connection
ws.onopen = function () {
    console.log('WebSocket connection established.');

    // Json to request info about the relevant tickers
    ws.send(JSON.stringify({
        "type": "subscribe",
        "product_ids": favTickers,
        "channels": [
            "ticker",
            {
                "name": "ticker",
                "product_ids": favTickers,
            }
        ]
    }));
};

// Handle WebSocket Responses
ws.onmessage = function (event) {
    // Response I recieve
    const message = JSON.parse(event.data);

    try {
        if (message.type === 'ticker' && favTickers.includes(message.product_id)) {
            // Get the element to manipulate
            const tickerValueElement = document.getElementById(`${message.product_id}_value`);
            const tickerPercentageElement = document.getElementById(`${message.product_id}_percentage`);

            // Get the price and Daily percentage change from the response
            if (tickerValueElement && tickerPercentageElement) {
                const price = message.price
                const openPrice = message.open_24h
                tickerPercentage = (((price - openPrice) / openPrice) * 100).toFixed(2);
                
                if (tickerPercentage > 0) {
                    tickerPercentageElement.style.backgroundColor = "#11a452";
                    
                } else if (tickerPercentage < 0) {
                    tickerPercentageElement.style.backgroundColor = "#ef415b";

                } else {
                    tickerPercentageElement.style.backgroundColor = "#93b8e1";
                }
                
                // Update the inner html of the elements
                tickerValueElement.innerHTML = price;
                tickerPercentageElement.innerHTML = tickerPercentage + "%"
            }
        }
    } catch (error) {
        console.log("WebSocket Error:", error);
    }
};

// Handle WebSocket close event
ws.onclose = function () {
    console.log('WebSocket connection closed.');
};