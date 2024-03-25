from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.trade, name="trade"),
    path('close_position/', views.close_position, name='close_position'),
]