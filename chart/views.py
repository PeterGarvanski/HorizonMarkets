from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def chart(request):
    """
    A view to return the Chart page of the website.
    """

    # Requests the logged in users data and uses it to query the databases
    user = request.user

    # All the relevant context the templates will need
    context = {
        # Add Something here
    }

    return render(request, 'chart/chart.html', context)