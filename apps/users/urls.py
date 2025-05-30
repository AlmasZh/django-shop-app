from django.urls import path
from . import views
from .views import UserListCreateView, UserDetailView

app_name = "users"

urlpatterns = [
    path('', views.index, name="home"),
    path('apply-seller/', views.seller_application, name='seller_application'),
    path('logout/', views.user_logout, name="logout"),
    path('toggle_like/<int:product_id>/', views.toggle_like, name="toggle_like"),
    path('update_profile/', views.update_profile, name="update_profile"),
] +  [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]



