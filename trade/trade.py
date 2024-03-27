import websocket
import base64
import hashlib
import hmac
import json
import time
import uuid
from cryptography.hazmat.primitives.serialization import load_pem_private_key

API_KEY = 'pd50R4mhRgsnBy4rHmUEG5ZxIjIMQsOh8aclJxjpTYCAehNEIDMfYWGIUkSjNxHA'
SECRET_KEY = 'vYiipCL4c1bK8MrvcpXnYhGVOyabupuByI83oItfXdBhbDjbwFBshNECdCfxvBoN'


def construct_signature_payload(params):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    return '&'.join([f"{param}={value}" for param, value in sorted_params])


def compute_signature(payload, secret_key):
    return hmac.new(secret_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()


def place_order_message(ws, message):
    print("Received message:", message)


def query_order_message(ws, message):
    print("Received message:", message)


def place_order_open(ws):
    print("Order webSocket connection opened")

    # Set up the request parameters
    order = {
        'id': str(uuid.uuid4()),
        'method': 'order.place',
        'params' : {
            'symbol': 'BTCUSDT',
            'side': 'BUY',
            'type': 'MARKET',
            'quantity': '0.1',
            'timestamp': int(time.time() * 1000),
            'apiKey': API_KEY,
        }
    }

    # Sign the request
    payload = construct_signature_payload(order['params'])
    signature = compute_signature(payload, SECRET_KEY)
    order['params']['signature'] = signature

    # Send the order message
    ws.send(json.dumps(order))


def query_order_open(ws):
    print("Query webSocket connection opened")

    # Set up the request parameters
    order = {
        'id': str(uuid.uuid4()),
        'method': 'order.status',
        'params' : {
            'symbol': 'BTCUSDT',
            'orderId': '7329516',
            'timestamp': int(time.time() * 1000),
            'apiKey': API_KEY,
        }
    }

    # Sign the request
    payload = construct_signature_payload(order['params'])
    signature = compute_signature(payload, SECRET_KEY)
    order['params']['signature'] = signature

    # Send the order message
    ws.send(json.dumps(order))


def place_order_close(ws):
    print("Order webSocket connection closed")


def query_order_close(ws):
    print("Query webSocket connection closed")


def place_order():
    # Create a WebSocket connection
    ws = websocket.WebSocketApp("wss://testnet.binance.vision/ws-api/v3",
                                on_message=place_order_message,
                                on_open=place_order_open,
                                on_close=place_order_close)

    ws.run_forever()


def query_order():
    # Create a WebSocket connection
    ws = websocket.WebSocketApp("wss://testnet.binance.vision/ws-api/v3",
                                on_message=query_order_message,
                                on_open=query_order_open,
                                on_close=query_order_close)

    ws.run_forever()