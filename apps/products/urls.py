from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.home, name="home"),
    path('manclothes/', views.manclothes, name='manclothes'),
    path('categories/',views.categories, name="categories"),
    path('register/',views.register,name='register'),
    path('itempage/',views.itempage,name='itempage'),
    path('girlclothes/',views.girlclothes,name='girlclothes'),
    path('questionnaire/',views.questionnaire,name='questionnaire'),
    path('clothesadd/',views.clothesadd,name='clothesadd'),
    path('personal/',views.personal, name="personal")
    
]



