from django.contrib import admin
from .models import Payment, BillingAddress

# Register your models here.
admin.site.register(Payment)
admin.site.register(BillingAddress)