from env import BINANCE_API_KEY, BINANCE_SECRET_KEY
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import OpenTrade, TradeHistory
from dashboard.models import UserProfile, AccountHistory
import base64
import requests
import time
import datetime
from cryptography.hazmat.primitives.serialization import load_pem_private_key


@login_required
def trade(request):
    """
    A view to return the Trade page of the website,
    this includes a trading display where orders can be placed.
    This also allows users to monitor todays positions
    and any current open positions.
    """
    # Requests the logged in users data
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    error_message = ''

    # If a form is being submitted
    if request.method == 'POST':
        symbol = str(request.POST.get('symbol')).upper()
        side = str(request.POST.get('side'))
        order_type = str(request.POST.get('order-type'))
        quantity = float(request.POST.get('quantity'))
        take_profit = float(request.POST.get('take-profit'))
        stop_loss = float(request.POST.get('stop-loss'))
        price = request.POST.get('price')

        # If the trade is bullish place an order
        if side == 'BUY':
            trade = place_order(symbol, side, order_type, quantity, price)
            
            # If the order goes through create a new trade and post to the database
            if trade.get('status') == 'FILLED':
                new_trade = OpenTrade.objects.create(
                    user=user,
                    order_id=trade.get('orderId'),
                    client_order_id=trade.get('clientOrderId'),
                    symbol=trade.get('symbol'),
                    order_type=trade.get('type'),
                    side=trade.get('side'),
                    quantity=trade.get('executedQty'),
                    cumulative_quote_qty=trade.get('cummulativeQuoteQty'),
                    price=trade.get('price'),
                    take_profit=take_profit,
                    stop_loss=stop_loss
                )
                new_trade.save()
            
            # If trade did not get filled update error message
            else:
                print(trade)
                error_message = trade

        # If the trade is bearish check the assests and quantitys
        else:
            ...

    open_trades = []

    # Add open trades in a list to be displayed by template
    for trade in OpenTrade.objects.filter(user=user):
        order = {
            'id': str(trade.order_id),
            'time': str(trade.time.strftime('%H:%M')),
            'symbol': str(trade.symbol),
            'side': str(trade.side),
            'entry': round(float(trade.cumulative_quote_qty) / float(trade.quantity), 4),
            'take_profit': float(trade.take_profit),
            'stop_loss': float(trade.stop_loss)
        }
        open_trades.append(order)

    # All the relevant context the templates will need
    context = {
        'open_trades': open_trades,
        'account_balance': user_profile.account_balance,
        'error_message': error_message
    }

    return render(request, 'trade/trade.html', context)


def place_order(symbol, side, order_type, quantity, price):
    
    # Set up authentication
    API_KEY='UNIIeocODwpSIvGREzz2nvkx8QTietRueGTOTnI1nb5fqCcYW8uMzMWlvXIxijxG'
    PRIVATE_KEY_PATH='test-prv-key.pem'

    # Load the private key.
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = load_pem_private_key(data=f.read(),
                                        password=None)

    # Set up the request parameters
    if order_type == "MARKET":
        params = {
            'symbol':       symbol,
            'side':         side,
            'type':         order_type,
            'quantity':     quantity,
        }
    
    # Set up the request parameters
    else:
        params = {
            'symbol':       symbol,
            'side':         side,
            'type':         order_type,
            'quantity':     quantity,
            'price':        price,
            'timeInForce':  'GTC'
        }

    # Timestamp the request
    timestamp = int(time.time() * 1000)
    params['timestamp'] = timestamp

    # Sign the request
    payload = '&'.join([f'{param}={value}' for param, value in params.items()])
    signature = base64.b64encode(private_key.sign(payload.encode('ASCII')))
    params['signature'] = signature

    # Send the request
    headers = {
        'X-MBX-APIKEY': API_KEY,
    }
    response = requests.post(
        'https://testnet.binance.vision/api/v3/order',
        headers=headers,
        data=params,
    )
    return response.json()


def close_position(request):
    """
    A Function to close open trades,
    places an equal but opposite position to the one 
    selected, effectively closing the position,
    then redirects to trade page.
    """
    # Requests the logged in users data
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # If a form is being submitted get the open trade
    if request.method == 'POST':
        trade_id = request.POST.get('close_position')
        trade = OpenTrade.objects.filter(
            user=user,
            order_id=trade_id
        )[0]
        # Place an equal but oppopsite order
        opposite_trade = place_order(trade.symbol, 'SELL', 'MARKET', trade.quantity, 0)

        # If the order gets filled create a new entry for trade history
        if opposite_trade.get('status') == 'FILLED':
                net_pl = float(trade.cumulative_quote_qty) - float(opposite_trade.get('cummulativeQuoteQty'))

                new_trade = TradeHistory.objects.create(
                    user=user,
                    order_id=opposite_trade.get('orderId'),
                    client_order_id=opposite_trade.get('clientOrderId'),
                    symbol=opposite_trade.get('symbol'),
                    order_type=opposite_trade.get('type'),
                    quantity=opposite_trade.get('executedQty'),
                    cumulative_quote_qty=opposite_trade.get('cummulativeQuoteQty'),
                    price=opposite_trade.get('price'),
                    take_profit=trade.take_profit,
                    stop_loss=trade.stop_loss,
                    close_price='1',
                    net_pl=net_pl
                )
                new_trade.save()

                # Update user profile
                user_profile.account_balance = float(user_profile.account_balance) + float(net_pl)
                user_profile.save()

                # Update account history
                new_entry = AccountHistory.objects.create(
                    user=user,
                    new_account_balance=user_profile.account_balance,
                    net_difference=net_pl
                )
                new_entry.save()
                trade.delete()

    return redirect('trade')