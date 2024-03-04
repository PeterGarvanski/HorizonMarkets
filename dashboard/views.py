from django.shortcuts import render, redirect
from .forms import UserProfileForm, TransactionForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def dashboard(request):
    """
    A view to return the users personal dashboard,
    this includes a account history chart as well as the
    users assortment of personal tickers and their data.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # All the relevant context the templates will need
    context = {
        "account_balance" : user_profile.account_balance,
        "account_history" : "50000,45789,36789,42516,52456,59123,61123,65930,68234,70123,67282,65929",
        "fav_tickers" : ["BTC", "ETH", "BNB", "SOL", "USDC", "ADA", "AVAX", "DOT"],
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
def settings(request):
    """
    A view to return the settings page of the website,
    this includes a section where the users can submit a
    form for customer support.
    """

    # All the relevant context the templates will need
    context = {
        # Add something here
    }

    return render(request, 'dashboard/settings.html', context)


@login_required
def transfer(request):
    """
    A view to return the Transfer page of the website,
    this includes two forms: one where customers can
    make deposits and withdrwals and another where they
    can update their personal information.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    transaction_form = TransactionForm()
    
    # If a form is being submitted
    if request.method == 'POST':

        # If the form is the Transaction form get that form
        if 'country' in request.POST:
            transaction_form = TransactionForm(request.POST)

            # If all the form fields are valid get the data
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)

                # If the transfer_type is deposit add money to account
                if transaction.transfer_type == "Deposit":
                    user_profile.account_balance = (user_profile.account_balance + transaction.amount)
                    user_profile.save()

                # If the transfer_type is withdraw subtract money from account
                else:
                    user_profile.account_balance = (user_profile.account_balance - transaction.amount)
                    user_profile.save()

                # Post users transactions to the database and redirect to dashboard
                transaction.user = user
                transaction.save()
                return redirect('dashboard')

            # If form is invalid send error message
            else:
                error_message = "Transaction Form is Invalid!"

        # If the form is the UserProfile form get that form
        else:
            settings_form = UserProfileForm(request.POST, instance=user)

            # If all the form fields are valid post data and redirect
            if settings_form.is_valid():
                settings_form.save()
                return redirect('dashboard')
            
            # If form is invalid send error message
            else:
                error_message = "User Profile Form is Invalid!"

    # If method is GET pre-populate userProfile form
    else:
        settings_form = UserProfileForm(instance=user)
        error_message = ""

    # All the relevant context the templates will need
    context = {
        "stripe_public_key": "pk_test_51OiF1tJWloYFxaUMwarc2ylIFT2HDdMBdhIoQ90gX5ys75vKPeH14zg1rs4dMriikfWXMgxMa429xi22q4tvVhi200Ckh9XClc",
        "client_secret": "sk_test_51OiF1tJWloYFxaUMA4g6SWVtSdaTb0x4wMTmnSX1KxMMwxOGKbaOQkvSbMTMScTqnIKm9Hgq4GnVDW5X6o6Wr00j00vJKwFWp0",
        "transaction_form": transaction_form,
        "settings_form": settings_form,
        "error_message": error_message,
    }

    return render(request, 'dashboard/transfer.html', context)
