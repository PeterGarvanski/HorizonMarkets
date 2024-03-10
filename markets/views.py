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

    # Empty list to store the query results
    crypto_query  = []

    # If a form is being submitted
    if request.method == 'POST':

        # If the form is the search bar look up the asset and return a query
        if 'search_bar' in request.POST:
            search_response = request.POST.get('search_bar')
            for asset in all_assets['cryptos']:
                crypto, currency = asset.split("/")

                # If the search directly matches the crypto just return the market
                if search_response.upper() == crypto:
                    market.user_market = asset
                    market.save()

                # Otherwise return a query with potential cryptos
                elif search_response.upper() in asset:
                    crypto_query.append(asset)
        
        # If the form is the crypto options save the ticker to user_market
        elif 'crypto_name' in request.POST:
            chosen_market = request.POST.get('crypto_name')
            market.user_market = chosen_market
            market.save()

        # If the form is the favourites add the ticker to fav_tickers
        elif 'add_to_favourites' in request.POST:
            crypto, currency = market.user_market.split("/")
            if len(market.fav_tickers) < 8 and crypto not in market.fav_tickers:
                market.fav_tickers.append(crypto)
                market.save()

        # If the form is the remove ticker, remove the ticker from fav_tickers
        elif 'remove_crypto' in request.POST:
            crypto = request.POST.get('remove_crypto')
            market.fav_tickers.remove(crypto)
            market.save()
            return redirect('dashboard')

    # Modify the names fior user freindability
    users_market = market.user_market
    modified_market = users_market.replace("/", "")
    crypto, currency = users_market.split("/")

    # Sets is_favourited depending if the ticker is already in fav_tickers
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