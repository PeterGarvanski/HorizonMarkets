from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from .forms import UserProfileForm, TransactionForm
from .models import UserProfile, AccountHistory
from markets.models import Market
import stripe
from env import STRIPE_SECRET_KEY
from datetime import datetime
import calendar


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
    account_history_querys = AccountHistory.objects.filter(user=user)
    fav_tickers = Market.objects.get_or_create(user=user)[0]

    # Create timestamps for day, month and year for later use
    today = datetime.now().date()
    this_month = datetime.now().month
    this_year = datetime.now().year

    # Calculate days in month and create lists for months and days for later use
    days_in_month = calendar.monthrange(this_year, this_month)[1]
    days_in_month_list = [day for day in range(1, days_in_month + 1)]
    months = [calendar.month_name[month] for month in range(1, 13)]
    daily_balances_in_month = [0 for _ in days_in_month_list]
    monthly_balances_in_year = [0 for _ in months]

    # Creates a value to prepopulate the day chart for the account history
    try:
        initial_account_balance_today = account_history_querys.exclude(
            date=today
        ).latest('date', 'time').new_account_balance
    
    except ObjectDoesNotExist:
        initial_account_balance_today = 0

    # Create a dictionary to store sorted account history data
    account_history = {
        'today': {'balances': [float(initial_account_balance_today)], 'times': ['Start of Today']},
        'this_month': {'balances': daily_balances_in_month, 'days': days_in_month_list},
        'this_year': {'balances': monthly_balances_in_year, 'months': months}
    }

    # Sorts account history data based on dates and times into the dictionary
    for data in account_history_querys:
        date = data.date
        time = data.time.strftime('%H:%M')
        balance = data.new_account_balance

        # Today's account history
        if date == today:
            account_history['today']['balances'].append(float(balance))
            account_history['today']['times'].append(str(time))

        # This Months account history
        if date.month == this_month and date.year == this_year:

            # For each day in the month create a custom date and query the database
            for day in days_in_month_list:
                custom_date = f'{this_year}-{this_month}-{day}'
                balance_for_day = AccountHistory.objects.filter(
                    user=user,
                    date=custom_date
                ).last()

                # If the balance has changed that day set its value to the corresponding day in the list
                if balance_for_day:
                    daily_balances_in_month[day - 1] = float(balance_for_day.new_account_balance)

                # Otherwise find the last existing balance before the current day
                else:
                    previous_balance = AccountHistory.objects.filter(
                        user=user,
                        date__lt=custom_date
                    ).order_by('-date', '-time').first()
                    
                    # If there are balances set the value to the previous existing balance
                    if previous_balance:
                        daily_balances_in_month[day - 1] = float(previous_balance.new_account_balance)
                    
                    # If there's no previous balance, set it to 0
                    else:
                        daily_balances_in_month[day - 1] = 0

        # This Years account history
        if date.year == this_year:

            # For each month in the year query the database and get the last monthly transaction
            for month in range(len(months)):
                last_monthly_balance = AccountHistory.objects.filter(
                    user=user, 
                    date__year=this_year,
                    date__month=(month + 1)
                ).last()

                # If there are transactions this month set the new value to the corresponding month
                if last_monthly_balance:
                    monthly_balances_in_year[month] = float(last_monthly_balance.new_account_balance)

                # If there are no transactions this month get the value of the last transaction made
                else:
                    previous_monthly_balance = AccountHistory.objects.filter(
                        user=user, 
                        date__year=this_year,
                    ).last()

                    query_year, query_month, query_day = str(previous_monthly_balance.date).split("-")

                    # If the user has previous transactions and no transactions this month
                    if previous_monthly_balance and month > int(query_month) - 1:
                        monthly_balances_in_year[month] = float(previous_monthly_balance.new_account_balance)

                    # If the user has no transactions
                    else:
                        monthly_balances_in_year[month] = 0

    # All the relevant context the templates will need
    context = {
        'account_balance' : user_profile.account_balance,
        'account_history' : account_history,
        'fav_tickers' : fav_tickers.fav_tickers,
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
    make deposits and withdrawals and another where they
    can update their personal information.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    account_history_querys = AccountHistory.objects.filter(user=user)
    transaction_form = TransactionForm()
    settings_form = UserProfileForm(instance=user)
    error_message = ''  # Initialize error_message here

    # If a form is being submitted
    if request.method == 'POST':

        # If the form is the Transaction form get that form
        if 'country' in request.POST:
            transaction_form = TransactionForm(request.POST)

            # If all the form fields are valid get the data
            if transaction_form.is_valid():
                transaction = transaction_form.save(commit=False)

                # If the transfer_type is deposit add money to account
                if transaction.transfer_type == 'Deposit':
                    user_profile.account_balance = (user_profile.account_balance + transaction.amount)
                    new_entry = AccountHistory.objects.create(
                        user=user,
                        new_account_balance=user_profile.account_balance,
                        net_difference=transaction.amount
                    )

                    user_profile.save()
                    new_entry.save()

                # If the transfer_type is withdraw subtract money from account
                else:
                    user_profile.account_balance = (user_profile.account_balance - transaction.amount)
                    new_entry = AccountHistory.objects.create(
                        user=user,
                        new_account_balance=user_profile.account_balance,
                        net_difference=transaction.amount
                    )

                    user_profile.save()
                    new_entry.save()

                # Post users transactions to the database and redirect to dashboard
                transaction.user = user
                transaction.save()
                return redirect('dashboard')

            # If form is invalid send error message
            else:
                error_message = 'Transaction Form is Invalid!'

        # If the form is the UserProfile form get that form
        else:
            settings_form = UserProfileForm(request.POST, instance=user)

            # If all the form fields are valid post data and redirect
            if settings_form.is_valid():
                settings_form.save()
                return redirect('dashboard')
            
            # If form is invalid send error message
            else:
                error_message = 'User Profile Form is Invalid!'

    # All the relevant context the templates will need
    context = {
        'transaction_form': transaction_form,
        'settings_form': settings_form,
        'error_message': error_message,
    }

    return render(request, 'dashboard/transfer.html', context)


# This is your test secret API key.
stripe.api_key = STRIPE_SECRET_KEY

YOUR_DOMAIN = 'https://8000-petergarvan-horizonmark-ofungvqkje6.ws-eu110.gitpod.io/'

def create_checkout_session(request):
    try:
        # Your code to create the checkout session goes here
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    'price': 'price_1OuZR3P1CjHWdbKH01S6Ap9A',
                    'quantity': 1,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN,
        )
        return JsonResponse({'clientSecret': session.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def session_status():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))

  return JsonResponse(status=session.status, customer_email=session.customer_details.email)
