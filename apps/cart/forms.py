from django import forms
from apps.products.models import Product
from apps.cart.models import CartItem

class CartUpdateForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1, 
        widget=forms.NumberInput(attrs={
            'class': 'px-3 py-1 border rounded-md w-16 text-center'
        })
    )
    remove = forms.BooleanField(required=False, widget=forms.HiddenInput())



"""
from django import forms
from .models import CartItem, Cart

class AddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        min_value=1, 
        initial=1, 
        widget=forms.NumberInput(attrs={
            'class': 'hidden', 
            'id': 'quantity-input'
        })
    )
    size = forms.ChoiceField(
        choices=[
            ('XS', 'XS'),
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border rounded-md flex justify-between items-center',
            'id': 'size-select'
        })
    )
    color = forms.ChoiceField(
        choices=[
            ('beige', 'Beige'),
            ('black', 'Black'),
            ('white', 'White')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full p-3 border rounded-md flex justify-between items-center',
            'id': 'color-select'
        })
    )

    class Meta:
        model = CartItem
        fields = ['quantity', 'product']

    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['product'].initial = product
"""