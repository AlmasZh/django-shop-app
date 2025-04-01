from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from apps.products.models import Product
from .forms import UserProfileUpdateForm, SellerApplicationForm
from django.contrib import messages
from .models import SellerApplication

# Create your views here.
def index(request):
    return render(request, 'users/index.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('products:home')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Redirect to profile page
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'profile_update_modal.html', {'form': form})

@login_required
def toggle_like(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)

    if product in user.likes.all():
        user.likes.remove(product)
    else:
        user.likes.add(product)

    # return HttpResponse()
    return redirect('products:products_detail', slug=product.slug)

@login_required
def seller_application(request):
    if request.method == 'POST':
        form = SellerApplicationForm(request.POST)
        seller_app = SellerApplication.objects.filter(user=request.user, status='PENDING').first()
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_manager or request.user.is_staff:
                messages.error(request, 'You are already a seller!')
                return redirect('products:personal_my_products')
            if seller_app:
                messages.error(request, 'You have already applied to be a seller!')
                return redirect('products:personal_my_products')
            application.user = request.user
            application.save()
            return redirect('products:personal_my_products')  # Define this URL later
    else:
        form = SellerApplicationForm(user=request.user)
    
    return render(request, 'users/seller_application.html', {'form': form})