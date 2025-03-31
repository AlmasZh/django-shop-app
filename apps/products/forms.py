from django import forms
from .models import Category, Product
from .models import ProductImage
from django.core.validators import FileExtensionValidator


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
    gender = forms.ChoiceField(
        choices=[
            ('unisex', 'Unisex'),
            ('men', 'Men'),
            ('women', 'Women'),
        ],
        required=False
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
            ('XS', 'Extra Small'),
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
            ('XXL', 'Double Extra Large'),
            ('3XL', 'Triple Extra Large'),
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

class ProductForm(forms.ModelForm):
    PRODUCT_TYPES = [
        ('tshirt', 'T-shirt'),
        ('jeans', 'Jeans'),
        ('dress', 'Dress'),
        ('jacket', 'Jacket'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('perfume', 'Perfume'),
    ]
    COLORS = [
        ('black', 'Black'),
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('gray', 'Gray'),
        ('brown', 'Brown'),
        ('other', 'Other'),
    ]
    SIZES = [
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    ]
    
    # Fields remain the same as in your original code
    title = forms.CharField(
        max_length=200, 
        widget=forms.TextInput(attrs={
            'class': 'form-input', 
            'placeholder': 'Enter brand name',
            'id': 'brandName',
            'required': True
        })
    )
    price = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        widget=forms.NumberInput(attrs={
            'class': 'form-input', 
            'placeholder': '0.00',
            'step': '0.01',
            'id': 'price',
            'required': True
        })
    )
    product_category = forms.ChoiceField(
        choices=PRODUCT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'productType',
            'required': True
        })
    )
    color = forms.ChoiceField(
        choices=COLORS,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'color',
            'required': True
        })
    )
    size = forms.ChoiceField(
        choices=SIZES,
        widget=forms.Select(attrs={
            'class': 'form-select w-full border-gray-300 rounded-md',
            'id': 'size-select',
            'required': True
        })
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea', 
            'rows': '3',
            'placeholder': 'Enter material details (e.g., 100% cotton, polyester blend, etc.)',
            'id': 'description'
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'file-input', 
            'accept': 'image/*', 
            'id': 'productImages'
        })
    )
    
    class Meta:
        model = Product
        fields = ['title', 'price', 'product_category', 'color', 'size', 'description', 'image']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        # Ensure a category is set - you might want to modify this logic
        try:
            category = Category.objects.first()
            if not category:
                raise ValueError("No categories exist. Please create a category first.")
        except Category.DoesNotExist:
            raise ValueError("No categories exist. Please create a category first.")
        
        # Save the product
        product = super().save(commit=False)
        product.category = category
        
        # Set the user if provided
        if self.user:
            product.user = self.user
        
        if commit:
            product.save()
        
        # Handle single image upload
        image = self.cleaned_data.get('image')
        if image:
            ProductImage.objects.create(
                product=product, 
                image=image,
                is_main=True  # First image is set as main
            )
        
        return product