from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.signup_view, name="signup"),
]

