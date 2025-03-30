import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopApp.settings')
django.setup()

from apps.products.models import Category

# Create main categories
main_categories = ['Clothes', 'Accessories', 'Shoes', 'Perfumes']
for title in main_categories:
    Category.objects.get_or_create(title=title, is_sub=False)

# Get the Clothes category
clothes_cat = Category.objects.get(title='Clothes')

# Create subcategories for Clothes
sub_categories = [
    'Tops',
    'Bottoms',
    'Dresses',
    'Outerwear',
    'Activewear',
    'Swimwear',
    'Sleepwear',
    'Formal Wear',
]
for sub_title in sub_categories:
    Category.objects.get_or_create(title=sub_title, sub_category=clothes_cat, is_sub=True)