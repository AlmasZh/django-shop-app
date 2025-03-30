from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name="home"),
    path('logout/', views.user_logout, name="logout"),
    path('toggle_like/<int:product_id>/', views.toggle_like, name="toggle_like"),
    path('update_profile/', views.update_profile, name="update_profile"),
]

