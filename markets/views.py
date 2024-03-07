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
    market = Market.objects.get_or_create(user=user)[0]

    crypto_query  = []

    if request.method == 'POST':

        if 'search_bar' in request.POST:
            search_response = request.POST.get('search_bar')
            for crypto in all_assets['cryptos']:
                if search_response.upper() in crypto:
                    crypto_query.append(crypto)
        
        elif 'crypto_name' in request.POST:
            chosen_market = request.POST.get('crypto_name')
            market.user_market = chosen_market
            market.save()

        elif 'add_to_favourites' in request.POST:
            crypto, currency = market.user_market.split("/")
            if len(market.fav_tickers) < 8 and crypto not in market.fav_tickers:
                market.fav_tickers.append(crypto)
                market.save()

        elif 'remove_crypto' in request.POST:
            crypto = request.POST.get('remove_crypto')
            market.fav_tickers.remove(crypto)
            market.save()
            return redirect('dashboard')

        elif 'add_to_chart' in request.POST:
            ...

    users_market = market.user_market
    modified_market = users_market.replace("/", "")
    crypto, currency = users_market.split("/")

    if crypto in market.fav_tickers:
        is_favourited = True
    else: 
        is_favourited = False

    # All the relevant context the templates will need
    context = {
        'crypto_querys' : crypto_query[0:5],
        'user_market' : modified_market,
        'is_favourited' : is_favourited
    }

    return render(request, 'markets/market.html', context)