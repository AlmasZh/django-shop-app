from django import forms
from apps.users.models import CustomUser
from django.core.exceptions import ValidationError
from .models import SellerApplication
from django.contrib.auth import authenticate

style = 'w-full px-3 py-1 border rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500'

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )

    def clean(self):
        """
        Custom validation to authenticate user
        """
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise ValidationError("Invalid email or password")
        
        return cleaned_data

class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'John',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Doe',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        }),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary'
        })
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            raise ValidationError({
                "confirm_password": "Passwords do not match"
            })

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Last Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Phone Number',
                'type': 'tel'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email Address'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance
        
        # Check if email is already taken by another user
        if CustomUser.objects.exclude(pk=user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        
        return email

class SellerApplicationForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Store the user if needed
    
    class Meta:
        model = SellerApplication
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[120px]',
                'placeholder': 'Tell us about your store: what categories of clothes do you sell, what are the features?'
            }),
        }
    
    