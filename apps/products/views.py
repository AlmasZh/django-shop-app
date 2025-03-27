from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth import authenticate, login
from apps.users.forms import LoginForm, RegistrationForm

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

def itempage(request):
    return render(request,'products/itempage.html')

def girlclothes(request):
    return render(request,'products/Girlclothes.html')

def questionnaire(request):
    return render(request,'products/questionnaire.html')

def clothesadd(request):
    return render(request,'products/clothesadd.html')

def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj


def home_page(request):
	products = Product.objects.all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


# def product_detail(request, slug):
# 	# form = QuantityForm()
# 	product = get_object_or_404(Product, slug=slug)
# 	related_products = Product.objects.filter(category=product.category).all()[:5]
# 	context = {
# 		'title':product.title,
# 		'product':product,
# 		'form':form,
# 		'favorites':'favorites',
# 		'related_products':related_products
# 	}
# 	if request.user.likes.filter(id=product.id).first():
# 		context['favorites'] = 'remove'
# 	return render(request, 'product_detail.html', context)


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


def search(request):
	query = request.GET.get('q')
	products = Product.objects.filter(title__icontains=query).all()
	context = {'products': paginat(request ,products)}
	return render(request, 'home_page.html', context)


def filter_by_category(request, slug):
	"""when user clicks on parent category
	we want to show all products in its sub-categories too
	"""
	result = []
	category = Category.objects.filter(slug=slug).first()
	[result.append(product) \
		for product in Product.objects.filter(category=category.id).all()]
	if not category.is_sub:
		sub_categories = category.sub_categories.all()
		for category in sub_categories:
			[result.append(product) \
				for product in Product.objects.filter(category=category).all()]
	context = {'products': paginat(request ,result)}
	return render(request, 'home_page.html', context)
