import websocket
import json


def on_message(ws, message):
    data = json.loads(message)
    # Process incoming data here
    print(data)


def on_error(ws, error):
    print(error)


def on_open(ws):
    # Subscribe to tickers
    ws.send(json.dumps(
        {
        "method": "SUBSCRIBE",
        "params": ["btcusdt@trade", "ethusdt@trade"],
        "id": 1}
    ))


def on_close(ws):
    print("### closed ###")


def on_error(ws, error):
    print(error)


def on_message(ws, message):
    data = json.loads(message)
    # Process incoming data here
    print(data)


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws", on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()