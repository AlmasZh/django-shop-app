from django import forms
from .models import Category, Product

class ProductFilterForm(forms.Form):
    PRICE_CHOICES = [
        ('', 'All Prices'),
        ('low', 'Low to High'),
        ('high', 'High to Low'),
    ]
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        required=False, 
        empty_label="All Categories"
    )
    color = forms.ChoiceField(
        choices=[
            ('', 'All Colors'),
            ('white', 'White'),
            ('black', 'Black'),
            # Add more colors as needed
        ],
        required=False
    )
    size = forms.ChoiceField(
        choices=[
            ('', 'All Sizes'),
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
        ],
        required=False
    )
    price_order = forms.ChoiceField(
        choices=PRICE_CHOICES,
        required=False
    )
    discount_only = forms.BooleanField(
        required=False,
        label="Only Discounted Items"
    )