from django.shortcuts import render


def index(request):
    """
    A view to return the dashboard page of the website.
    """
    return render(request, 'dashboard/index.html')
