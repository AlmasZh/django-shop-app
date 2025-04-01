from django import forms
from .models import Category, Product
from .models import ProductImage, Review
from django.forms.models import inlineformset_factory


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

    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter product title',
            'id': 'title',
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
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_sub=False),  # Only top-level categories
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'category',
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

    class Meta:
        model = Product
        fields = ['title', 'price', 'category', 'color', 'size', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:
            product.user = self.user
        if commit:
            product.save()
        return product

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'file-input',
                'accept': 'image/*',
                'id': 'productImage'
            }),
            'is_main': forms.CheckboxInput(attrs={
                'class': 'form-checkbox'
            })
        }

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,  # Number of empty image forms to display by default
    can_delete=False  # No deletion for simplicity; add True if you want to allow it
)



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border rounded', 'placeholder': 'Review Title'}),
            'comment': forms.Textarea(attrs={'class': 'w-full p-2 border rounded', 'rows': 4, 'placeholder': 'Write your review here...'}),
        }