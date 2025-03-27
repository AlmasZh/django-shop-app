from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.products.models import Product
from .models import Cart, CartItem
from django.contrib import messages

# Create your views here.
@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': request.POST.get('quantity', 1)}
    )
    
    # If the item already exists, update its quantity
    if not item_created:
        cart_item.quantity += int(request.POST.get('quantity', 1))
        cart_item.save()
    
    messages.success(request, f"{product.title} added to cart!")
    return redirect('products:products_detail', slug=slug)