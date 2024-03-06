from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Market
from .assets import all_assets


@login_required
def markets(request):
    """
    A view to return the Markets page of the website,
    this includes a searchbar allowing users to search
    favourite and view simplistic charts of cryptos.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user
    market = Market.objects.get_or_create(user=user)

    crypto_query  = []

    if request.method == 'POST':
        search_response = request.POST.get('search_bar')
        for crypto in all_assets['cryptos']:
            if search_response.upper() in crypto:
                crypto_query.append(crypto)


    # All the relevant context the templates will need
    context = {
        'crypto_querys' : crypto_query
    }

    return render(request, 'markets/market.html', context)