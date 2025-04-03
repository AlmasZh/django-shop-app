from rest_framework import serializers
from .models import Category, Product, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'sub_category', 'is_sub', 'slug']
        read_only_fields = ['id', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'user', 'category', 'gender', 'title', 'brand_name',
            'description', 'price', 'season', 'size', 'color', 'pattern',
            'origin_country', 'date_created', 'slug'
        ]
        read_only_fields = ['id', 'date_created', 'slug']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'product', 'user', 'rating', 'title', 'comment',
            'is_approved', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']