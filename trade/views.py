from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def trade(request):
    """
    A view to return the Trade page of the website,
    """

    # All the relevant context the templates will need
    context = {
        ...
    }

    return render(request, 'trade/trade.html')
