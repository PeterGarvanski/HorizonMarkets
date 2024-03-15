from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('settings/', views.settings, name="settings"),
    path('transfer/', views.transfer, name="transfer"),
    path('create-checkout-session/', views.create_checkout_session, name="checkout_session"),
    path('session-status/', views.session_status, name="session_status"),
]