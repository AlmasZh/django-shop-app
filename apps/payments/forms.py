# payments/forms.py
from django import forms
from .models import BillingAddress

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['street_address', 'apartment_address', 'country', 'state', 'city', 'zip']