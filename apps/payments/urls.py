# payments/urls.py
from django.urls import path
from .views import checkout_view
from django.shortcuts import render

app_name = 'payments'

urlpatterns = [
    path('process/', checkout_view, name='process'),
    path('success/', lambda request: render(request, 'payments/success.html'), name='order_success'),
    # Add other URLs as needed
]