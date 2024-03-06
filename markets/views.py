from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def markets(request):
    """
    A view to return the Markets page of the website,
    this includes a searchbar allowing users to search
    favourite and view simplistic charts of cryptos.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user

    # All the relevant context the templates will need
    context = {
        # Add Something here
    }

    return render(request, 'markets/market.html', context)