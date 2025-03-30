from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from apps.users.forms import LoginForm, RegistrationForm
from apps.products.forms import ProductFilterForm
from apps.products.models import Product, ProductImage, Category
from apps.users.forms import UserProfileUpdateForm
from apps.cart.models import Cart, CartItem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProductForm
from apps.cart.forms import CartUpdateForm

from apps.products.models import Product, Category
# from apps import QuantityForm

def home(request):
    return render(request, 'products/index.html')

def manclothes(request):
    return render(request, 'products/Manclothes.html')

def categories(request):
    return render(request,'products/categories.html')

def register(request):
    register_form = RegistrationForm()
    form = LoginForm()

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

def personal(request):
    return render(request,'products/personal.html')

def products_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product_images = ProductImage.objects.filter(product=product)
    
    context = {
        'product': product,
        'product_images': product_images,
        'liked_products': request.user.likes.all() if request.user.is_authenticated else [],
    }
    return render(request, 'products/product_detail.html', context)



def girlclothes(request):
    return render(request,'products/Girlclothes.html')

def questionnaire(request):
    return render(request,'products/questionnaire.html')

def add_product(request):
    """
    View function to handle product creation.
    
    This view allows authenticated users to add new products to the system.
    """
    if request.method == 'POST':
        # Pass the current user to the form during initialization
        form = ProductForm(request.POST, request.FILES, user=request.user)
        
        if form.is_valid():
            try:
                # Save the product with the current user
                product = form.save()
                
                messages.success(request, f'Product "{product.title}" was successfully added.')
                return redirect('products:personal_my_products')
            
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {
        'form': form,
        'categories': Category.objects.all()
    })

# 	p = Paginator(list_objects, 20)
# 	page_number = request.GET.get('page')
# 	try:
# 		page_obj = p.get_page(page_number)
# 	except PageNotAnInteger:
# 		page_obj = p.page(1)
# 	except EmptyPage:
# 		page_obj = p.page(p.num_pages)
# 	return page_obj


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


# def filter_by_category(request, slug):
# 	"""when user clicks on parent category
# 	we want to show all products in its sub-categories too
# 	"""
# 	result = []
# 	category = Category.objects.filter(slug=slug).first()
# 	[result.append(product) \
# 		for product in Product.objects.filter(category=category.id).all()]
# 	if not category.is_sub:
# 		sub_categories = category.sub_categories.all()
# 		for category in sub_categories:
# 			[result.append(product) \
# 				for product in Product.objects.filter(category=category).all()]
# 	context = {'products': paginat(request ,result)}
# 	return render(request, 'home_page.html', context)

def product_list(request):
    # Base queryset of all products
    products = Product.objects.all()
    
    # Initialize filter form
    filter_form = ProductFilterForm(request.GET)
    
    # Apply filters if form is valid
    if filter_form.is_valid():
        # Category filter
        if filter_form.cleaned_data['category']:
            products = products.filter(category=filter_form.cleaned_data['category'])
        
        # Price ordering
        if filter_form.cleaned_data['price_order'] == 'low':
            products = products.order_by('price')
        elif filter_form.cleaned_data['price_order'] == 'high':
            products = products.order_by('-price')
        
        # Discount filter
        if filter_form.cleaned_data['discount_only']:
            products = products.filter(discount_price__isnull=False)
    
    # Pagination
    paginator = Paginator(products, 30)  # 30 items per page
    
    # Get the current page number
    page = request.GET.get('page', 1)
    
    try:
        # Try to get the specific page
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paginated_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        paginated_products = paginator.page(paginator.num_pages)
    
    context = {
        'products': paginated_products,
        'filter_form': filter_form,
        'categories': Category.objects.all(),
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
    return render(request, 'products/personal_cart.html')

def personal_my_products(request): 
    user_products = Product.objects.filter(user=request.user)
    return render(request, 'products/personal_my_products.html', {
        'user_products': user_products,
        # 'user': request.user
    })

def personal_moderation(request):
    return render(request, 'products/personal_moderation.html')

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