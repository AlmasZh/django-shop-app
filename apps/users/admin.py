from django.contrib import admin
# Register your models here.

from .models import CustomUser, SellerApplication

admin.site.register(CustomUser)
admin.site.register(SellerApplication)