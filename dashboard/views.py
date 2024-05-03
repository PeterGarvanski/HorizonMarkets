# from env import STRIPE_SECRET_KEY, PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY, SENDER_EMAIL, RECIPIENT_EMAIL
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserProfileForm
from .models import UserProfile, AccountHistory
from markets.models import Market
from trade.models import TradeHistory
import stripe
import requests
from datetime import datetime
import calendar
import time
import uuid
import json

STRIPE_SECRET_KEY = settings.STRIPE_SECRET_KEY
PAYPAL_CLIENT_ID = settings.PAYPAL_CLIENT_ID
PAYPAL_SECRET_KEY = settings.PAYPAL_SECRET_KEY
SENDER_EMAIL = settings.SENDER_EMAIL
RECIPIENT_EMAIL = settings.RECIPIENT_EMAIL

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
def customer_support(request):
    """
    A function that allows users to send emails to customer support
    """
    # Requests the logged in users data and uses it to query the databases
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # If the user form is being submitted
    if request.method == 'POST':
        subject = request.POST.get('subject')
        body = request.POST.get('body') + f'\nAccount Email: {user_profile.email}'
        send_mail(
            subject,
            body,
            SENDER_EMAIL,
            [RECIPIENT_EMAIL],
            fail_silently=False,
        )

    return redirect('dashboard')


@login_required
def deposit(request):
    """
    A view to return the Transfer page of the website,
    this includes a stripe payment form allowing users
    to deposit money into their accounts.
    """

    # Requests the logged in users data
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # If the form is being submitted change the users amount_multiplier
    if request.method == 'POST':
        amount_multiplier = request.POST.get('amount-multiplier')
        user_profile.deposit_amount_multiplier = amount_multiplier
        user_profile.save()

    # All the relevant context the templates will need
    context = {
        'multiplier': user_profile.deposit_amount_multiplier
    }

    return render(request, 'dashboard/deposit.html', context)


@login_required
def withdraw(request):
    """
    A view to return the Withdraw page of the website,
    this includes a payment form allowing users
    to withdraw money into their accounts.
    """
    # Requests the logged in users data
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    access_token = get_access_token(PAYPAL_CLIENT_ID, PAYPAL_SECRET_KEY)

    # If the form is being get the email and amount from the fields
    if request.method == 'POST':
        email = request.POST.get('paypal-email')
        withdrawal_amount = request.POST.get('withdrawal-amount')

        # Headers and Data for paypal payout system
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }

        data = {
            "sender_batch_header": {
                "sender_batch_id": f"Payouts_{time.strftime('%Y%m%d%H%M%S')}",
                "email_subject": "You have money!",
                "email_message": "You received a payment. Thanks for using our service!"
            },
            "items": [
                {
                    "recipient_type": "EMAIL",
                    "amount": {
                        "value": f"{float(withdrawal_amount)}",
                        "currency": "USD"
                    },
                    "note": "Horizon Markets Withdrawal!",
                    "sender_item_id": f"Item_{uuid.uuid4()}",
                    "receiver": "sb-l2gaz29911579@personal.example.com",
                    "recipient_wallet": "PAYPAL"
                }
            ]
        }

        # Post the data and get the batch id from the response
        post_response = requests.post(
            'https://api-m.sandbox.paypal.com/v1/payments/payouts',
            headers=headers,
            data=json.dumps(data)
        )
        post_response_data = post_response.json()
        payout_batch_id = post_response_data['batch_header']['payout_batch_id']

        # Gets JSON response
        response = requests.get(f'https://api-m.sandbox.paypal.com/v1/payments/payouts/{payout_batch_id}', headers=headers)
        response_data = response.json()

        # If the withdrawal went through
        if response_data['batch_header']['batch_status'] == 'PENDING' or response_data['batch_header']['batch_status'] == 'SUCCESS':
            
            # Update users account balance
            user_profile.account_balance = float(user_profile.account_balance) - float(withdrawal_amount)
            user_profile.save()

            # Log a new entry to account history
            new_entry = AccountHistory.objects.create(
                user=user,
                new_account_balance=user_profile.account_balance,
                net_difference=withdrawal_amount
            )
            new_entry.save()

            return redirect('dashboard')

    # All the relevant context the templates will need
    context = {
        'account_balance': user_profile.account_balance
    }

    return render(request, 'dashboard/withdraw.html', context)


@login_required
def account_transactions(request):
    """
    A view to return all account history entries
    """
    # Requests the logged in users data
    user = request.user
    querys = AccountHistory.objects.filter(user=user)

    account_historys = []
    for entry in querys:
        account_historys.append(
            {
                'new_balance': entry.new_account_balance,
                'net_diffrence': entry.net_difference,
                'date': entry.date,
                'time': entry.time
            }
        )

    # All the relevant context the templates will need
    context = {
        'account_historys': account_historys
    }

    return render(request, 'dashboard/account-transactions.html', context)


@login_required
def trading_logs(request):
    """
    A view to return all account history entries
    """
    # Requests the logged in users data
    user = request.user
    querys = TradeHistory.objects.filter(user=user)

    trading_logs = []
    for entry in querys:
        trading_logs.append(
            {
                'time' : entry.time,
                'date' : entry.date,
                'order_id' : entry.order_id,
                'symbol' : entry.symbol,
                'type' : entry.order_type,
                'quantity' : entry.quantity,
                'quote' : round(entry.cumulative_quote_qty, 2),
                'entry' : round(entry.entry_price, 2),
                'close' : round(entry.close_price, 2),
                'take_profit' : round(entry.take_profit, 2),
                'stop_loss' : round(entry.stop_loss, 2),
                'net_pl' : round(entry.net_pl, 2),
            }
        )

    # All the relevant context the templates will need
    context = {
        'trading_logs': trading_logs
    }

    return render(request, 'dashboard/trading-logs.html', context)


@login_required
def return_page(request):

    return render(request, 'dashboard/return.html')


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


def get_access_token(client_id, client_secret):
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'  # For production, use 'https://api.paypal.com/v1/oauth2/token'
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    auth = (client_id, client_secret)
    response = requests.post(url, headers=headers, data=data, auth=auth)
    
    if response.status_code == 200:
        print('Access Token Aquired')
        return response.json()['access_token']
    else:
        print('Error:', response.text)
        return None