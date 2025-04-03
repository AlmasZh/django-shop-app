from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from apps.users.models import SellerApplication
from apps.users.forms import UserProfileUpdateForm, LoginForm, RegistrationForm
from apps.cart.models import Cart, CartItem
from apps.cart.forms import CartUpdateForm
from .forms import ProductForm, ProductImageFormSet, ReviewForm, ProductFilterForm
from .models import Product, ProductImage, Category, Review

# from apps import QuantityForm

def home(request):
    return render(request, 'products/index.html')

def manclothes(request):
    return render(request, 'products/Manclothes.html')

def categories(request):
    return render(request,'products/categories.html')

def girlclothes(request):
    return render(request,'products/Girlclothes.html')

def personal(request):
    return render(request,'products/personal.html')

def product_search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query)
        ).order_by('-date_created')
    else:
        products = Product.objects.all().order_by('-date_created')
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'products/search_results.html', context)

def register(request):
    register_form = RegistrationForm()
    form = LoginForm()
    if request.user.is_authenticated:
        return redirect('products:personal_orders')

    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('first_name'):
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                print("user is saved")
                messages.success(request, 'Account created successfully!')
                return redirect('products:home')
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
				# Authenticate user (assuming you've set up custom authentication backend)
                user = authenticate(request, username=email, password=password)
				
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.')
                    return redirect('products:home')  # Redirect to home page after login
    return render(request, 'products/Register.html', {'form': form, 'register_form': register_form})


def products_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = ProductImage.objects.filter(product=product)
    reviews = Review.objects.filter(product=product)
    
    # Review form handling
    review_form = ReviewForm()
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            try:
                review.save()
            except IntegrityError:
                messages.error(request, 'You have already reviewed this product.')
            else:
                messages.success(request, 'Your review has been submitted for approval.')
            return redirect('products:products_detail', slug=slug)

    context = {
        'product': product,
        'product_images': product_images,
        'reviews': reviews,
        'review_form': review_form,
        'liked_products': request.user.likes.all() if request.user.is_authenticated else [],
    }
    print(reviews)
    return render(request, 'products/product_detail.html', context)

@login_required
def review_delete(request, slug, review_id):
    product = get_object_or_404(Product, slug=slug)
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
    return redirect('products:products_detail', slug=slug)

@login_required
def review_edit(request, slug, review_id):
    product = get_object_or_404(Product, slug=slug)
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Review updated successfully.')
            return redirect('products:products_detail', slug=slug)
    else:
        form = ReviewForm(instance=review)
    
    context = {
        'product': product,
        'review_form': form,
        'review': review,
    }
    return render(request, 'products/review_edit.html', context)


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, user=request.user)
        image_formset = ProductImageFormSet(request.POST, request.FILES)
        if form.is_valid() and image_formset.is_valid():
            product = form.save()  # Save the product first
            image_formset.instance = product  # Link the formset to the saved product
            image_formset.save()  # Save all images
            print("slug: ", product.slug)
            return redirect('products:products_detail', slug=product.slug)  # Adjust redirect as needed
    else:
        form = ProductForm(user=request.user)
        image_formset = ProductImageFormSet()
    
    return render(request, 'products/add_product.html', {
        'form': form,
        'image_formset': image_formset
    })

@login_required
def add_to_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.add(product)
	return redirect('shop:product_detail', slug=product.slug)


@login_required
def remove_from_favorites(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	request.user.likes.remove(product)
	return redirect('shop:favorites')


@login_required
def favorites(request):
	products = request.user.likes.all()
	context = {'title':'Favorites', 'products':products}
	return render(request, 'favorites.html', context)


# def search(request):
# 	query = request.GET.get('q')
# 	products = Product.objects.filter(title__icontains=query).all()
# 	context = {'products': paginat(request ,products)}
# 	return render(request, 'home_page.html', context)

# def product_list(request):
#     # Base queryset of all products
#     products = Product.objects.all()
    
#     # Initialize filter form
#     filter_form = ProductFilterForm(request.GET)
    
#     # Apply filters if form is valid
#     if filter_form.is_valid():
#         if filter_form.cleaned_data['category']:
#             products = products.filter(category=filter_form.cleaned_data['category'])
#         if filter_form.cleaned_data['gender']:
#             products = products.filter(gender=filter_form.cleaned_data['gender'])
#         if filter_form.cleaned_data['color']:
#             products = products.filter(color=filter_form.cleaned_data['color'])
#         if filter_form.cleaned_data['size']:
#             products = products.filter(size=filter_form.cleaned_data['size'])
#         if filter_form.cleaned_data['price_order'] == 'low':
#             products = products.order_by('price')
#         elif filter_form.cleaned_data['price_order'] == 'high':
#             products = products.order_by('-price')
#         if filter_form.cleaned_data['discount_only']:
#             products = products.filter(discount_price__isnull=False)
    
#     # Pagination
#     paginator = Paginator(products, 30)
#     page = request.GET.get('page', 1)
#     try:
#         paginated_products = paginator.page(page)
#     except PageNotAnInteger:
#         paginated_products = paginator.page(1)
#     except EmptyPage:
#         paginated_products = paginator.page(paginator.num_pages)
    
#     # Create query string without 'page'
#     query_params = request.GET.copy()
#     if 'page' in query_params:
#         del query_params['page']
#     query_string = query_params.urlencode()
    
#     context = {
#         'products': paginated_products,
#         'filter_form': filter_form,
#         'categories': Category.objects.all(),
#         'query_string': query_string,
#     }
#     return render(request, 'products/product_list.html', context)

def product_list(request):
    # Base queryset of all products
    products = Product.objects.all()
    
    # Initialize filter form
    filter_form = ProductFilterForm(request.GET)
    
    # Get search query
    search_query = request.GET.get('q', '').strip()
    
    # Apply filters if form is valid
    if filter_form.is_valid():
        # Apply search filter first if there's a query
        if search_query:
            products = products.filter(title__icontains=search_query)
            
        # Apply other filters
        if filter_form.cleaned_data['category']:
            products = products.filter(category=filter_form.cleaned_data['category'])
        if filter_form.cleaned_data['gender']:
            products = products.filter(gender=filter_form.cleaned_data['gender'])
        if filter_form.cleaned_data['color']:
            products = products.filter(color=filter_form.cleaned_data['color'])
        if filter_form.cleaned_data['size']:
            products = products.filter(size=filter_form.cleaned_data['size'])
        if filter_form.cleaned_data['price_order'] == 'low':
            products = products.order_by('price')
        elif filter_form.cleaned_data['price_order'] == 'high':
            products = products.order_by('-price')
        if filter_form.cleaned_data['discount_only']:
            products = products.filter(discount_price__isnull=False)
    
    # Pagination
    paginator = Paginator(products, 30)
    page = request.GET.get('page', 1)
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)
    
    # Create query string without 'page'
    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']
    query_string = query_params.urlencode()
    
    context = {
        'products': paginated_products,
        'filter_form': filter_form,
        'categories': Category.objects.all(),
        'query_string': query_string,
        'search_query': search_query,  # Add search query to context
    }
    return render(request, 'products/product_list.html', context)


def personal_orders(request):
    return render(request, 'products/personal_orders.html')

def personal_likes(request):
    favorite_products = request.user.likes.all()
    return render(request, 'products/personal_likes.html', {
        'favorite_products': favorite_products
    })

def personal_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    
    if request.method == 'POST':
        form = CartUpdateForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            quantity = form.cleaned_data['quantity']
            remove = form.cleaned_data['remove']
            
            product = Product.objects.get(id=product_id)
            
            if remove:
                CartItem.objects.filter(cart=cart, product=product).delete()
            else:
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, 
                    product=product
                )
                cart_item.quantity = quantity
                cart_item.save()
            
            return redirect('products:personal_cart')
    
    cart_items = cart.items.all()
    total_price = cart.total_price()
    
    return render(request, 'products/personal_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_update_form': CartUpdateForm()
    })

def personal_my_products(request): 
    user_products = Product.objects.filter(user=request.user)
    return render(request, 'products/personal_my_products.html', {
        'user_products': user_products,
    })

def personal_update(request):
    user = request.user  # Get the currently logged-in user
    
    if request.method == "POST":
        form = UserProfileUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("products:personal_orders")  # Redirect to the user's profile page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserProfileUpdateForm(instance=user)

    return render(request, "products/personal_update.html", {"form": form})

##

def is_admin(user):
    return user.is_staff or user.is_manager

@login_required
@user_passes_test(is_admin)
def personal_moderation(request):
    applications = SellerApplication.objects.all().select_related('user')
    return render(request, 'products/personal_moderation.html', {'applications': applications})

@login_required
@user_passes_test(is_admin)
def update_application_status(request, application_id, action):
    if request.method != 'POST':
        try:
            application = SellerApplication.objects.get(id=application_id)
            user = application.user
            if action == 'approve':
                application.status = 'approved'
                user.is_manager = True
                user.save()
            elif action == 'reject':
                application.status = 'rejected'
            else:
                return messages.error(request, 'Invalid action')
            application.save()
            messages.success(request, 'Application status updated successfully')
            return redirect('products:personal_moderation') 
        except SellerApplication.DoesNotExist:
            return messages.error(request, 'Application not found')