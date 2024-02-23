from django.shortcuts import render, redirect
from .forms import UserProfileForm
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
        "account_balance": user_profile.account_balance,
        "account_history": "50000,45789,36789,42516,52456,59123,61123,65930,68234,70123,67282,65929",
        "fav_tickers" : ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "ADA-USD","DOT-USD", "USDT-USD", "LINK-USD"],
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def settings(request):
    """
    A view to return the dashboard page of the website.
    """
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            # Update custom UserProfile fields
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            return redirect('settings')
    else:
        # Prepopulate the form with existing user data
        initial_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

        form = UserProfileForm(instance=user, initial=initial_data)

    context = {
        "form": form,
    }

    return render(request, 'dashboard/settings.html', context)


def transfer(request):
    """
    A view to return the Transfer page of the website.
    """
    return render(request, 'dashboard/transfer.html')