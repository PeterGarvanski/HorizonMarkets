from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('settings/', views.settings, name="settings"),
    path('customer-support/', views.customer_support, name='customer_support'),
    path('deposit/', views.deposit, name="deposit"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('create-checkout-session/', views.create_checkout_session, name="checkout_session"),
    path('session-status/', views.session_status, name="session_status"),
    path('return.html', views.return_page, name="return_page"),
]