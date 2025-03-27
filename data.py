import os
import django
import random
from django.core.files.base import ContentFile
from faker import Faker
from io import BytesIO
from PIL import Image, ImageDraw
import uuid

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopApp.settings')
django.setup()
from django.template.defaultfilters import slugify
from apps.products.models import Category, Product, ProductImage

# Initialize Faker
fake = Faker()

# Define lists for random attributes
SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']
COLORS = [
    'Red', 'Blue', 'Green', 'Yellow', 'Black', 'White', 'Gray', 
    'Navy', 'Purple', 'Pink', 'Orange', 'Brown', 'Beige'
]
SEASONS = ['Spring', 'Summer', 'Autumn', 'Winter']
PATTERNS = [
    'Solid', 'Striped', 'Checkered', 'Polka Dot', 
    'Floral', 'Geometric', 'Camouflage', 'Plaid'
]
COUNTRIES = [
    'USA', 'China', 'Italy', 'Vietnam', 'Bangladesh', 
    'India', 'Turkey', 'Germany', 'Portugal', 'Cambodia'
]

def create_categories():
    main_categories = [
        'T-Shirts', 'Shirts', 'Pants', 'Jackets', 'Accessories'
    ]
    
    created_categories = []
    for cat_name in main_categories:
        category, created = Category.objects.get_or_create(
            title=cat_name,
            defaults={'is_sub': False}
        )
        created_categories.append(category)
        
        # Create some subcategories
        if cat_name == 'T-Shirts':
            subcats = ['Casual', 'Sports', 'Formal']
            for subcat in subcats:
                Category.objects.get_or_create(
                    title=f'{cat_name} - {subcat}',
                    defaults={
                        'sub_category': category,
                        'is_sub': True
                    }
                )
    
    return created_categories

def create_dummy_image(product_title):
    """Generates a dummy image for a product"""
    # Generate a random background color
    color = (
        random.randint(100, 220), 
        random.randint(100, 220), 
        random.randint(100, 220)
    )
    
    # Create image
    image = Image.new('RGB', (400, 600), color=color)
    draw = ImageDraw.Draw(image)
    
    # Add product name text
    draw.text((20, 20), product_title, fill=(0, 0, 0))
    
    # Save image to a file
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    
    filename = f'{uuid.uuid4()}.png'
    django_file = ContentFile(buffer.getvalue(), name=filename)
    
    return django_file, filename

def create_products(categories, num_products=300):
    """Create sample products with multiple images and random attributes"""
    for _ in range(num_products):
        # Choose a random category
        category = random.choice(categories)
        
        # Generate product details
        product_title = fake.catch_phrase()
        
        # Avoid duplicate slugs
        unique_slug = slugify(product_title)
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{unique_slug}-{random.randint(1, 1000)}'
        
        # Create product with random attributes
        product = Product.objects.create(
            category=category,
            title=product_title,
            description=fake.paragraph(nb_sentences=3),
            price=round(random.uniform(10.00, 500.00), 2),
            slug=unique_slug,
            # Add random attributes
            size=random.choice(SIZES),
            color=random.choice(COLORS),
            season=random.choice(SEASONS),
            pattern=random.choice(PATTERNS),
            origin_country=random.choice(COUNTRIES)
        )
        
        # Create multiple images for each product
        num_images = random.randint(2, 5)  # Each product gets 2-5 images
        for i in range(num_images):
            image_file, filename = create_dummy_image(product_title)
            is_main = (i == 0)  # First image is the main image
            ProductImage.objects.create(
                product=product,
                image=image_file,
                is_main=is_main
            )

def main():
    # Clear existing data (optional, be careful!)
    Product.objects.all().delete()
    Category.objects.all().delete()
    ProductImage.objects.all().delete()
    
    # Create categories
    categories = create_categories()
    
    # Create products
    create_products(categories)
    
    print(f"Data Generation Complete!")
    print(f"Categories created: {Category.objects.count()}")
    print(f"Products created: {Product.objects.count()}")
    print(f"Product images created: {ProductImage.objects.count()}")

if __name__ == '__main__':
    main()