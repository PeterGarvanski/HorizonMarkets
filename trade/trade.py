import websocket
import hashlib
import hmac
import json
import time
import uuid
from cryptography.hazmat.primitives.serialization import load_pem_private_key


API_KEY = 'eVCKz8VvUi2FCSlxbuV3LT54cWVPa4OVU6ycVVEu0AyBXUHbG4RJmTNfxnqXaBPQ'
SECRET_KEY = 'kR9m1gC574eV5SUz1LrSGpQ1ul0kDi3NF3PrKHaCmcqY0wIw2HbY390E1l9YvBRy'


def construct_signature_payload(params):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    return '&'.join([f'{param}={value}' for param, value in sorted_params])


def compute_signature(payload, secret_key):
    return hmac.new(secret_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()


def trade_on_message(ws, response):
    print('Received message:', response)

    if response.get('status') == 'FILLED':
        print(True)
    
    ws.close()


def trade_on_open(ws, params):
    print('Order webSocket connection opened')

    # Sign the request
    payload = construct_signature_payload(params['params'])
    signature = compute_signature(payload, SECRET_KEY)
    params['params']['signature'] = signature

    # Send the order message
    ws.send(json.dumps(params))


def trade_on_close(ws):
    print('Order webSocket connection closed')


def handle_trade(params, symbol, side, quantity, price, take_profit, stop_loss):

    if params == 'MARKET':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'order.place',
            'params' : {
                'symbol': symbol,
                'side': side,
                'type': 'MARKET',
                'quantity': quantity,
                'timestamp': int(time.time() * 1000),
                'apiKey': API_KEY,
            }
        }

    elif params == 'LIMIT':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'order.place',
            'params' : {
                'symbol': symbol,
                'side': side,
                'type': 'LIMIT',
                'price': price,
                'quantity': quantity,
                'timeInForce': 'GTC',
                'timestamp': int(time.time() * 1000),
                'apiKey': API_KEY,
            }
        }

    elif params == 'OPEN_ORDERS':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'openOrders.status',
            'params': {
                'symbol': symbol,
                'timestamp': int(time.time() * 1000),
                'apiKey': API_KEY,
            }
        }

    elif params == 'CANCEL_OPEN_ORDERS':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'openOrders.cancelAll',
            'params': {
                'symbol': symbol,
                'timestamp': int(time.time() * 1000),
                'apiKey': API_KEY,
            }
        }

    elif params == 'ORDER_STATUS':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'order.status',
            'params': {
                'symbol': symbol,
                'orderId': '3090331',
                'timestamp': int(time.time() * 1000),
                'apiKey': API_KEY,
            }
        }

    # Create a WebSocket connection
    ws = websocket.WebSocketApp('wss://testnet.binance.vision/ws-api/v3',
                                on_message=trade_on_message,
                                on_open=lambda ws: trade_on_open(ws, request_message),
                                on_close=trade_on_close)

    ws.run_forever()


handle_trade('MARKET', 'BNBUSDT', 'BUY', '1', '', '', '')