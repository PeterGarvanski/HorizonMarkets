from django.shortcuts import render, redirect
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    """
    A view to return the dashboard page of the website.
    """

    context = {
        "fav_tickers" : ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD","DOT-USD", "USDT-USD", "LINK-USD"],
    }
    return render(request, 'dashboard/dashboard.html', context)


def settings(request):
    """
    A view to return the Settings page of the website.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')  # Redirect to a success page
    else:
        form = UserProfileForm()

    context = {
        "form" : form
    }

    return render(request, 'dashboard/settings.html', context)


def transfer(request):
    """
    A view to return the Transfer page of the website.
    """
    return render(request, 'dashboard/transfer.html')