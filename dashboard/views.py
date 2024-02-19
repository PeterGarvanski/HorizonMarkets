from django.shortcuts import render


def dashboard(request):
    """
    A view to return the dashboard page of the website.
    """

    context = {
        "fav_tickers" : ["BTC", "ETH", "SOL", "XRP", "ADA", "NEXO", "USDT", "GBPX"],
    }
    return render(request, 'dashboard/dashboard.html', context)
