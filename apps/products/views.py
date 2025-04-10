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
from apps.orders.models import Order
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


# def personal_orders(request):
#     orders = Order.objects.filter(user=request.user).order_by('-created')
#     return render(request, 'products/personal_orders.html', {'orders': orders})
# def personal_orders(request):
#     orders = Order.objects.filter(user=request.user)  # Adjust query as needed
#     status_sequence = ['pending', 'processing', 'shipped', 'delivered']
#     return render(request, 'products/personal_orders.html', {
#         'orders': orders,
#         'status_sequence': status_sequence,
#     })

def personal_orders(request):
    if request.user.is_superuser or request.user.is_manager:
        products = Product.objects.filter(user=request.user)
        orders = Order.objects.all().prefetch_related('status_history')
    else:
        orders = Order.objects.filter(user=request.user).prefetch_related('status_history')
    normal_sequence = ['pending', 'processing', 'shipped', 'delivered']
    
    for order in orders:
        roadmap = []
        if order.delivery_status != 'cancelled':
            # Non-cancelled: Show full sequence with status markings
            try:
                current_index = normal_sequence.index(order.delivery_status)
            except ValueError:
                current_index = -1  # Fallback, though unlikely with valid statuses
            for i, status in enumerate(normal_sequence):
                history_entry = order.status_history.filter(status=status).first()
                if i < current_index:
                    step_class = 'completed'
                elif i == current_index:
                    step_class = 'current'
                else:
                    step_class = 'future'
                roadmap.append({
                    'status': status,
                    'display': dict(Order.DELIVERY_STATUS_CHOICES)[status],
                    'timestamp': history_entry.timestamp if history_entry else None,
                    'step_class': step_class
                })
        else:
            # Cancelled: Show only "Cancelled"
            cancelled_entry = order.status_history.filter(status='cancelled').first()
            roadmap.append({
                'status': 'cancelled',
                'display': 'Cancelled',
                'timestamp': cancelled_entry.timestamp if cancelled_entry else order.updated,
                'step_class': 'current'
            })
        order.roadmap = roadmap
    
    context = {'orders': orders}
    return render(request, 'products/personal_orders.html', context)

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

@login_required
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




######## API Views ########



from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .models import Review
from .serializers import ReviewSerializer


# Category Views
class CategoryListCreateView(APIView):
    @swagger_auto_schema(
        responses={200: CategorySerializer(many=True)},
        operation_description="Retrieve list of all categories"
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer(),
            400: 'Bad Request'
        },
        operation_description="Create a new category"
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={
            200: CategorySerializer(),
            404: 'Not Found'
        },
        operation_description="Retrieve a specific category"
    )
    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CategorySerializer,
        responses={
            200: CategorySerializer(),
            400: 'Bad Request',
            404: 'Not Found'
        },
        operation_description="Update a specific category"
    )
    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        operation_description="Delete a specific category"
    )
    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Product Views
class ProductListCreateView(APIView):
    @swagger_auto_schema(
        responses={200: ProductSerializer(many=True)},
        operation_description="Retrieve list of all products"
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={
            201: ProductSerializer(),
            400: 'Bad Request'
        },
        operation_description="Create a new product"
    )
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={
            200: ProductSerializer(),
            404: 'Not Found'
        },
        operation_description="Retrieve a specific product"
    )
    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses={
            200: ProductSerializer(),
            400: 'Bad Request',
            404: 'Not Found'
        },
        operation_description="Update a specific product"
    )
    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        operation_description="Delete a specific product"
    )
    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class ReviewListCreateView(APIView):
    @swagger_auto_schema(
        responses={200: ReviewSerializer(many=True)},
        operation_description="Retrieve a list of all reviews ordered by creation date"
    )
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        responses={
            201: ReviewSerializer(),
            400: 'Bad Request - Invalid data or duplicate review'
        },
        operation_description="Create a new review. Ensures unique user-product combination."
    )
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={
            200: ReviewSerializer(),
            404: 'Review not found'
        },
        operation_description="Retrieve a specific review by ID"
    )
    def get(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        responses={
            200: ReviewSerializer(),
            400: 'Bad Request - Invalid data',
            404: 'Review not found'
        },
        operation_description="Update a specific review by ID"
    )
    def put(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: 'Review deleted successfully',
            404: 'Review not found'
        },
        operation_description="Delete a specific review by ID"
    )
    def delete(self, request, pk):
        review = self.get_object(pk)
        if review is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)