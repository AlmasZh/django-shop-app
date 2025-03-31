from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.home, name="home"),
    path('manclothes/', views.manclothes, name='manclothes'),
    path('shop/',views.product_list, name="shop"),
    path('register/',views.register, name='register'),
    path('products_detail/<str:slug>', views.products_detail, name='products_detail'),
    path('girlclothes/',views.girlclothes,name='girlclothes'),
    path('questionnaire/',views.questionnaire,name='questionnaire'),
    path('add_product/',views.add_product, name='add_product'),

    path('personal/update', views.personal_update, name="personal_update"),

    path('personal/orders', views.personal_orders, name="personal_orders"),
    path('personal/likes', views.personal_likes, name="personal_likes"),
    path('personal/cart', views.personal_cart, name="personal_cart"),
    path('personal/my_products', views.personal_my_products, name="personal_my_products"),
    # path('personal/my_products/add', views.personal_my_products_add, name="personal_my_products_add"),
    # path('personal/my_products/<int:product_id>/edit', views.personal_my_products_edit, name="personal_my_products_edit"),
    # path('personal/my_products/<int:product_id>/delete', views.personal_my_products_delete, name="personal_my_products_delete"),
    path('personal/moderation.html', views.personal_moderation, name="personal_moderation"),
]



