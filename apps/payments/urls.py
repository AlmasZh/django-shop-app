# payments/urls.py
from django.urls import path
from django.shortcuts import render
from .views import order_create_view, payment_process_view


app_name = 'payments'
urlpatterns = [
    path('create-order/', order_create_view, name='create_order'),
    path('process-payment/<int:order_id>/', payment_process_view, name='process_payment'),
    path('success/', lambda request: render(request, 'payments/success.html'), name='order_success'),
]