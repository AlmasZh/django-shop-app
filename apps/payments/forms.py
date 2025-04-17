# forms.py
from django import forms
from .models import BillingAddress

class BillingAddressForm(forms.ModelForm):
    class Meta:
        model = BillingAddress
        fields = ['street_address', 'city', 'zip', 'country']
        widgets ={
            'street_address':forms.TextInput(attrs={
                'class':'border-gray-400 border-[1px] rounded-[5px] w-[100%] p-[4px] pl-2',
                'placeholder':'Street Name, House Number'
                }),
            'city':forms.TextInput(attrs={
                'class':'border-gray-400 border-[1px] rounded-[5px] w-[100%] p-[4px] pl-2',
                'placeholder':'Almaty'
            }),
            'zip':forms.TextInput(attrs={
                'class':'border-gray-400 border-[1px] rounded-[5px] w-[100%] p-[4px] pl-2',
                'placeholder':'010000'
                                         }),
            'country':forms.TextInput(attrs={
                'class':'border-gray-400 border-[1px] rounded-[5px] w-[100%] p-[4px] pl-2',
                'placeholder':'Kazakhstan'
                }),
            
        }