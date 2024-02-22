from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('settings/', views.settings, name="settings"),
    path('transfer/', views.transfer, name="transfer"),
]