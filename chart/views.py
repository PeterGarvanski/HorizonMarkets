from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Chart
from django.contrib.auth.models import User


@login_required
def chart(request):
    """
    A view to return the Chart page of the website.
    This includes multiple charts to be able to view,
    draw and track positions.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user
    chart = Chart.objects.get_or_create(user=user)[0]

    # If a form is being submitted
    if request.method == "POST":
        
        # If the form is the remove chart form remove that crypto element from the database
        if 'remove_chart' in request.POST:
            crypto = request.POST.get('remove_chart')
            chart.crypto_charts.remove(crypto)
            chart.save()

        # If the form is the add chart form add that crypto element to the database
        if 'add_chart' in request.POST:
            crypto = request.POST.get('add_chart')
            chart.crypto_charts.append(crypto)
            chart.save()

    # All the relevant context the templates will need
    context = {
        'crypto_charts': chart.crypto_charts
    }

    return render(request, 'chart/chart.html', context)