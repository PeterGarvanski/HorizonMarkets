from env import BINANCE_API_KEY, BINANCE_SECRET_KEY
from .models import OpenTrade
import websocket
import hashlib
import hmac
import json
import time
import uuid
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def construct_signature_payload(params):
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    return '&'.join([f'{param}={value}' for param, value in sorted_params])


def compute_signature(payload, secret_key):
    return hmac.new(secret_key.encode('utf-8'), payload.encode('utf-8'), hashlib.sha256).hexdigest()


def trade_on_message(ws, response, user, take_profit, stop_loss):
    trade = json.loads(response)
    try:
        if trade.get('status') == 200:
            result = trade.get('result')
            new_trade = OpenTrade.objects.create(
                user=user,
                order_id=result.get('orderId'),
                client_order_id=result.get('clientOrderId'),
                symbol=result.get('symbol'),
                order_type=result.get('type'),
                side=result.get('side'),
                quantity=result.get('executedQty'),
                cumulative_quote_qty=result.get('cummulativeQuoteQty'),
                entry=(float(result.get('cummulativeQuoteQty')) / float(result.get('executedQty'))),
                take_profit=take_profit,
                stop_loss=stop_loss,
            )
            new_trade.save()
            ws.close()
        
        else:
            print('Error placing trade!', trade)
            ws.close()

    except Exception as e:
        print('Error saving trade to database:', e)
        ws.close()

    print('Order webSocket connection closed')


def trade_on_open(ws, params):
    print('Order webSocket connection opened')

    # Sign the request
    payload = construct_signature_payload(params['params'])
    signature = compute_signature(payload, BINANCE_SECRET_KEY)
    params['params']['signature'] = signature

    # Send the order message
    ws.send(json.dumps(params))


def handle_trade(user, params, symbol, side, quantity, price, take_profit, stop_loss):

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
                'apiKey': BINANCE_API_KEY,
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
                'apiKey': BINANCE_API_KEY,
            }
        }

    elif params == 'OPEN_ORDERS':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'openOrders.status',
            'params': {
                'symbol': symbol,
                'timestamp': int(time.time() * 1000),
                'apiKey': BINANCE_API_KEY,
            }
        }

    elif params == 'CANCEL_OPEN_ORDERS':
        request_message = {
            'id': str(uuid.uuid4()),
            'method': 'openOrders.cancelAll',
            'params': {
                'symbol': symbol,
                'timestamp': int(time.time() * 1000),
                'apiKey': BINANCE_API_KEY,
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
                'apiKey': BINANCE_API_KEY,
            }
        }

    # Create a WebSocket connection
    ws = websocket.WebSocketApp('wss://testnet.binance.vision/ws-api/v3',
                                on_message=lambda ws, msg: trade_on_message(ws, msg, user, take_profit, stop_loss),
                                on_open=lambda ws: trade_on_open(ws, request_message),
                               )

    ws.run_forever()