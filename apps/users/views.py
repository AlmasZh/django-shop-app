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
            desired_role = form.cleaned_data.get('desired_role')
            # if desired_role == 'courier':
            #     request.user.is_courier = True
            #     request.user.save()
            # elif desired_role == 'manager':
            #     request.user.is_manager = True
            #     request.user.save()
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


#### API Views ####



from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import CustomUser
from .serializers import CustomUserSerializer

class UserListCreateView(APIView):
    @swagger_auto_schema(
        responses={200: CustomUserSerializer(many=True)},
        operation_description="Retrieve list of all users"
    )
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={
            201: CustomUserSerializer(),
            400: 'Bad Request'
        },
        operation_description="Create a new user"
    )
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None

    @swagger_auto_schema(
        responses={
            200: CustomUserSerializer(),
            404: 'Not Found'
        },
        operation_description="Retrieve a specific user"
    )
    def get(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={
            200: CustomUserSerializer(),
            400: 'Bad Request',
            404: 'Not Found'
        },
        operation_description="Update a specific user"
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            204: 'No Content',
            404: 'Not Found'
        },
        operation_description="Delete a specific user"
    )
    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)