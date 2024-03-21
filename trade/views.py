from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import UserProfile, AccountHistory


@login_required
def trade(request):
    """
    A view to return the Trade page of the website,
    """
    # Requests the logged in users data
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        order_type = request.POST.get('order-type')
        side = request.POST.get('direction')
        symbol = request.POST.get('symbol')
        amount = request.POST.get('amount')
        take_profit = request.POST.get('take-profit')
        stop_loss = request.POST.get('stop-loss')
        # price = request.POST.get('price')  # Assuming price is part of the form

        print(
            order_type,
            side,
            symbol,
            amount,
            take_profit,
            stop_loss
        )

    # All the relevant context the templates will need
    context = {
        'account_balance': user_profile.account_balance
    }

    return render(request, 'trade/trade.html', context)
