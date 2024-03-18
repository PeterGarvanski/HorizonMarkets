from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from .forms import UserProfileForm
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
    A view to return the Settings page of the website,
    this includes the users personal information form,
    and a section where the user can email customer support.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_form = UserProfileForm(instance=user)
    error_message = ''

    # If the user form is being submitted
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)

        # If all the form fields are valid post data and redirect
        if user_form.is_valid():
            user_form.save()
            return redirect('dashboard')
            
        # If form is invalid send error message
        else:
            error_message = 'User Profile Form is Invalid!'

    # All the relevant context the templates will need
    context = {
        'user_form': user_form,
        'error_message': error_message,
    }

    return render(request, 'dashboard/settings.html', context)


@login_required
def deposit(request):
    """
    A view to return the Transfer page of the website,
    this includes a stripe payment form allowing users
    to deposit money into their accounts.
    """

    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        amount_multiplier = request.POST.get('amount-multiplier')
        user_profile.deposit_amount_multiplier = amount_multiplier
        user_profile.save()

    context = {
        'multiplier': user_profile.deposit_amount_multiplier
    }

    return render(request, 'dashboard/deposit.html', context)


@login_required
def withdraw(request):
    """
    A view to return the Transfer page of the website,
    this includes a stripe payment form allowing users
    to deposit money into their accounts.
    """

    return render(request, 'dashboard/withdraw.html')


@login_required
def create_checkout_session(request):
    """
    Stripe function to create checkout sessions.
    """
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # Stripe information
    YOUR_DOMAIN = 'https://8000-petergarvan-horizonmark-ofungvqkje6.ws-eu110.gitpod.io/'
    stripe.api_key = STRIPE_SECRET_KEY

    try:
        # Creates a new checkout session
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    'price': 'price_1OuZR3P1CjHWdbKH01S6Ap9A',
                    'quantity': user_profile.deposit_amount_multiplier,
                },
            ],
            mode='payment',
            return_url=YOUR_DOMAIN + '/return.html?session_id={CHECKOUT_SESSION_ID}',
        )
    
    # If any errors occur
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    # Return stripe secret key
    return JsonResponse({'clientSecret': session.client_secret})


@login_required
def session_status(request):
    """
    Stripe function to retreieve session details,
    and update users account balance and history
    depending on deposits and withdrawals.
    """
    # Requests the logged in users data and uses it to query the databases
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    stripe.api_key = STRIPE_SECRET_KEY
    session_id = request.GET.get('session_id')

    # Try to get session details
    try:
        session = stripe.checkout.Session.retrieve(session_id)

        # If payment has been confirmed update account balance and add a entry for account history
        if session and session.payment_status == "paid":
            deposit_amount = session.amount_total / 100
            user_profile.account_balance = float(user_profile.account_balance) + float(deposit_amount)
            user_profile.save()

            new_entry = AccountHistory.objects.create(
                user=user,
                new_account_balance=user_profile.account_balance,
                net_difference=deposit_amount
            )
            new_entry.save()

        return JsonResponse({'status': session.status, 'customer_email': session.customer_email})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def return_page(request):

    return render(request, 'dashboard/return.html')
