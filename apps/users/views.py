from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.products.models import Product

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

@login_required
def toggle_like(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)

    if product in user.likes.all():
        user.likes.remove(product)
    else:
        user.likes.add(product)

    return redirect('products:products_detail', slug=product.slug)