// Collecting and processing data from the backend
const dataElement = document.getElementsByClassName('fav-tickers')[0];
const cryptoList = dataElement.getAttribute('data');
const modifiedCryptoList = cryptoList.replace(/'/g, '"');
const favTickers = JSON.parse(modifiedCryptoList);
const firstHalf = favTickers.slice(0, 4);

const websocketEndpoint = 'wss://stream.binance.com:9443/ws';
const ws = new WebSocket(websocketEndpoint);

// Function to subscribe to the WebSocket stream
const getTickerPrices = (tickers) => {

    // Subscribing to ticker streams for the provided symbols
    ws.onopen = () => {
        tickers.forEach(ticker => {
            const streamName = `${ticker.toLowerCase()}usdt@ticker`;
            const subscriptionMsg = JSON.stringify({
                method: 'SUBSCRIBE',
                params: [streamName],
                id: 1
            });
            ws.send(subscriptionMsg);
        });
    };

    // Handling incoming data
    ws.onmessage = (event) => {
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
        };
    };

    // Handling errors
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
};

// Calling the function to subscribe to ticker streams
getTickerPrices(firstHalf);