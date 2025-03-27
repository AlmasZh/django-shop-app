from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.index, name="home"),
    path('toggle_like/<int:product_id>/', views.toggle_like, name="toggle_like"),
]

