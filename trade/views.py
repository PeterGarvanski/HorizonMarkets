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
from .trade import handle_trade


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
    todays_trades = TradeHistory.objects.filter(user=user, date=datetime.datetime.now().date())
    error_message = ''

    # If a form is being submitted
    if request.method == 'POST':
        symbol = str(request.POST.get('symbol')).upper()
        side = str(request.POST.get('side'))
        order_type = str(request.POST.get('order-type'))
        quantity = str(request.POST.get('quantity'))
        take_profit = str(request.POST.get('take-profit'))
        stop_loss = str(request.POST.get('stop-loss'))
        price = str(request.POST.get('price'))

        handle_trade(
            user=user,
            params=order_type,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            take_profit=take_profit,
            stop_loss=stop_loss
        )

    open_trades = []
    trade_historys = []

    # Add open trades in a list to be displayed by template
    for trade in OpenTrade.objects.filter(user=user):
        order = {
            'id': str(trade.order_id),
            'time': str(trade.time.strftime('%H:%M')),
            'symbol': str(trade.symbol),
            'side': str(trade.side),
            'quantity': str(trade.quantity),
            'entry': float(trade.entry),
            'take_profit': float(trade.take_profit),
            'stop_loss': float(trade.stop_loss)
        }
        open_trades.append(order)

    for trade in todays_trades:
        if len(trade_historys) < 9:
            trade_historys.insert(0, trade)
        else:
            trade_historys.pop()
            trade_historys.insert(0, trade) 

    # All the relevant context the templates will need
    context = {
        'open_trades': open_trades,
        'trade_historys': trade_historys,
        'account_balance': user_profile.account_balance,
        'error_message': error_message
    }

    return render(request, 'trade/trade.html', context)


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

        side = 'SELL' if trade.side == 'BUY' else 'BUY'

        handle_trade(
            user=user,
            params='MARKET',
            symbol=f'{trade.symbol}',
            side=f'{side}',
            quantity=f'{trade.quantity}',
            price='0',
            take_profit='0',
            stop_loss='0'
        )

        opposite_trade = OpenTrade.objects.filter(user=user).order_by('-time').first()
        net_pl = float(opposite_trade.cumulative_quote_qty) - float(trade.cumulative_quote_qty)

        # If the order gets filled create a new entry for trade history

        new_trade = TradeHistory.objects.create(
            user=user,
            order_id=opposite_trade.order_id,
            client_order_id=opposite_trade.client_order_id,
            symbol=opposite_trade.symbol,
            order_type=opposite_trade.order_type,
            quantity=opposite_trade.quantity,
            cumulative_quote_qty=opposite_trade.cumulative_quote_qty,
            entry_price=trade.entry,
            take_profit=trade.take_profit,
            stop_loss=trade.stop_loss,
            close_price=opposite_trade.entry,
            net_pl=net_pl
        )
        new_trade.save()

        # Update user profile
        user_profile.account_balance = float(user_profile.account_balance) + net_pl
        user_profile.save()

        # Update account history
        new_entry = AccountHistory.objects.create(
            user=user,
            new_account_balance=user_profile.account_balance,
            net_difference=net_pl
        )
        new_entry.save()
        trade.delete()
        opposite_trade.delete()

    return redirect('trade')