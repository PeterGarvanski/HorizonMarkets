from env import BINANCE_API_KEY, BINANCE_SECRET_KEY
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import UserProfile, AccountHistory
import base64
import requests
import time
from cryptography.hazmat.primitives.serialization import load_pem_private_key


@login_required
def trade(request):
    """
    A view to return the Trade page of the website,
    """
    # Requests the logged in users data
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        side = request.POST.get('direction')
        order_type = request.POST.get('order-type')
        quantity = request.POST.get('quantity')
        take_profit = request.POST.get('take-profit')
        stop_loss = request.POST.get('stop-loss')
        # price = request.POST.get('price')  # Assuming price is part of the form

        place_order(symbol, side, order_type, quantity, 0)

    # All the relevant context the templates will need
    context = {
        'account_balance': user_profile.account_balance
    }

    return render(request, 'trade/trade.html', context)

def place_order(symbol, side, order_type, quantity, price):
    
    # Set up authentication
    API_KEY='UNIIeocODwpSIvGREzz2nvkx8QTietRueGTOTnI1nb5fqCcYW8uMzMWlvXIxijxG'
    PRIVATE_KEY_PATH='test-prv-key.pem'

    # Load the private key.
    # In this example the key is expected to be stored without encryption,
    # but we recommend using a strong password for improved security.
    with open(PRIVATE_KEY_PATH, 'rb') as f:
        private_key = load_pem_private_key(data=f.read(),
                                        password=None)

    print(symbol, side, order_type, quantity, price)

    # Set up the request parameters
    params = {
        'symbol':       symbol,
        'side':         side,
        'type':         order_type,
        'quantity':     quantity,
    }

    # Timestamp the request
    timestamp = int(time.time() * 1000) # UNIX timestamp in milliseconds
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
    print(response.json())