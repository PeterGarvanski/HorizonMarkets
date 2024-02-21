from django.shortcuts import render


def dashboard(request):
    """
    A view to return the dashboard page of the website.
    """

    context = {
        "fav_tickers" : ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD","DOT-USD", "USDT-USD", "LINK-USD"],
    }
    return render(request, 'dashboard/dashboard.html', context)
