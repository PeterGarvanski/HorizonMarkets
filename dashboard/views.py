from django.shortcuts import render, redirect
from .forms import UserProfileForm, TransactionForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def dashboard(request):
    """
    A view to return the dashboard page of the website.
    """

    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    context = {
        "account_balance" : user_profile.account_balance,
        "account_history" : "50000,45789,36789,42516,52456,59123,61123,65930,68234,70123,67282,65929",
        "fav_tickers" : ["BTC", "ETH", "BNB", "SOL", "USDC", "ADA", "AVAX", "DOT"],
        "stripe_pk" : "pk_test_51OiF1tJWloYFxaUMwarc2ylIFT2HDdMBdhIoQ90gX5ys75vKPeH14zg1rs4dMriikfWXMgxMa429xi22q4tvVhi200Ckh9XClc",
        "stripe_sk" : "sk_test_51OiF1tJWloYFxaUMA4g6SWVtSdaTb0x4wMTmnSX1KxMMwxOGKbaOQkvSbMTMScTqnIKm9Hgq4GnVDW5X6o6Wr00j00vJKwFWp0",
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def settings(request):
    """
    A view to return the dashboard page of the website.
    """

    context = {
        #
    }

    return render(request, 'dashboard/settings.html', context)


@login_required
def transfer(request):
    """
    A view to return the Transfer page of the website.
    """
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    transaction_form = TransactionForm()
    
    if request.method == 'POST':
        if 'country' in request.POST:
            transaction_form = TransactionForm(request.POST)
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)
                transaction.user = user
                transaction.save()
                return redirect('dashboard')
        else:
            settings_form = UserProfileForm(request.POST, instance=user)
            if settings_form.is_valid():
                settings_form.save()
                return redirect('dashboard')
    else:
        settings_form = UserProfileForm(instance=user)

    context = {
        "stripe_public_key": "pk_test_51OiF1tJWloYFxaUMwarc2ylIFT2HDdMBdhIoQ90gX5ys75vKPeH14zg1rs4dMriikfWXMgxMa429xi22q4tvVhi200Ckh9XClc",
        "client_secret": "sk_test_51OiF1tJWloYFxaUMA4g6SWVtSdaTb0x4wMTmnSX1KxMMwxOGKbaOQkvSbMTMScTqnIKm9Hgq4GnVDW5X6o6Wr00j00vJKwFWp0",
        "transaction_form": transaction_form,
        "settings_form": settings_form
    }

    return render(request, 'dashboard/transfer.html', context)
