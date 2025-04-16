from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from apps.users.models import CustomUser, SellerApplication
from apps.products.models import Category, Product, ProductImage, Review

class UserManagerTest(TestCase):
    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email='', password='password123')

    def test_create_user(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(email='admin@example.com', password='admin123')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.check_password('admin123'))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

class CustomUserTest(TestCase):
    def test_likes_relationship(self):
        # Create a Category instance (assuming Category has a 'name' field)
        category = Category.objects.create(title='Test Category')

        # Create a Product instance with required fields
        product = Product.objects.create(
            category=category,           # Required foreign key
            title='Test Product',        # Required
            price=10.00,                 # Required
            description='A test product' # Optional, but included for clarity
        )

        # Create a CustomUser instance and add the product to likes
        user = CustomUser.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        user.likes.add(product)

        # Assert that the product is in the user's likes
        self.assertIn(product, user.likes.all())
class SellerApplicationTest(TestCase):
    def test_create_application(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123')
        application = SellerApplication.objects.create(user=user, description='I want to be a seller')
        self.assertEqual(application.status, 'pending')
        self.assertEqual(application.user, user)

    def test_str_method(self):
        user = CustomUser.objects.create_user(email='test@example.com', password='password123', first_name='John', last_name='Doe')
        application = SellerApplication.objects.create(user=user, description='Test application')
        self.assertEqual(str(application), 'John Doe')
    

class CategoryTest(TestCase):
    def test_slug_generation(self):
        category = Category.objects.create(title="Test Category")
        self.assertEqual(category.slug, "test-category")

    def test_subcategory_relationship(self):
        parent = Category.objects.create(title="Parent Category")
        sub = Category.objects.create(title="Sub Category", sub_category=parent, is_sub=True)
        self.assertEqual(sub.sub_category, parent)

    def test_str_method(self):
        category = Category.objects.create(title="Test Category")
        self.assertEqual(str(category), "Test Category")

class ProductTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.user = CustomUser.objects.create_user(email="test@example.com", password="password123")
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.save()

    def test_slug_generation(self):
        product = Product.objects.create(
            category=self.category,
            title="Test Product",
            description="A test product",
            price=10.00
        )
        self.assertEqual(product.slug, "test-product")

    def test_search_method(self):
        product1 = Product.objects.create(
            category=self.category,
            title="Apple",
            description="Fruit",
            price=1.00
        )
        product2 = Product.objects.create(
            category=self.category,
            title="Banana",
            description="Fruit",
            price=0.50
        )
        results = Product.objects.search("app")
        self.assertIn(product1, results)
        self.assertNotIn(product2, results)

    def test_get_main_image(self):
        product = Product.objects.create(
            category=self.category,
            title="Product with Images",
            description="Has images",
            price=20.00
        )
        image1 = ProductImage.objects.create(product=product, image="image1.jpg", is_main=False)
        image2 = ProductImage.objects.create(product=product, image="image2.jpg", is_main=True)
        self.assertEqual(product.get_main_image(), image2)

        # Test when no main image is set
        product.images.all().delete()
        image3 = ProductImage.objects.create(product=product, image="image3.jpg", is_main=False)
        image4 = ProductImage.objects.create(product=product, image="image4.jpg", is_main=False)
        self.assertEqual(product.get_main_image(), image3)  # Should return the first image

    def test_get_average_rating_and_count(self):
        product = Product.objects.create(
            category=self.category,
            title="Reviewed Product",
            description="Has reviews",
            price=15.00
        )
        another_user = CustomUser.objects.create_user(email="another@example.com", password="password123")
        review1 = Review.objects.create(
            product=product,
            user=self.user,
            rating=4,
            comment="Good product"
        )
        review2 = Review.objects.create(
            product=product,
            user=another_user,
            rating=5,
            comment="Excellent"
        )
        self.assertEqual(product.get_review_count(), 2)
        self.assertEqual(product.get_average_rating(), 4.5)

    def test_str_method(self):
        product = Product.objects.create(
            category=self.category,
            title="Test Product",
            description="A test product",
            price=10.00
        )
        self.assertEqual(str(product), "Test Product - test-product")

class ProductImageTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            title="Test Product",
            description="A test product",
            price=10.00
        )

    def test_image_creation(self):
        image = ProductImage.objects.create(product=self.product, image="test.jpg", is_main=True)
        self.assertEqual(str(image), f"{self.product.title} - {image.id}")

class ReviewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Test Category")
        self.product = Product.objects.create(
            category=self.category,
            title="Test Product",
            description="A test product",
            price=10.00
        )
        self.user = CustomUser.objects.create_user(email="test@example.com", password="password123")
        self.user.first_name = "Test"
        self.user.last_name = "User"
        self.user.save()

    def test_review_creation(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            comment="Average product"
        )
        self.assertEqual(review.get_rating_display(), "3 - Average")

    def test_unique_review_per_user_product(self):
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="First review"
        )
        with self.assertRaises(IntegrityError):
            Review.objects.create(
                product=self.product,
                user=self.user,
                rating=5,
                comment="Second review"
            )

    def test_rating_validation(self):
        with self.assertRaises(ValidationError):
            review = Review(
                product=self.product,
                user=self.user,
                rating=6,
                comment="Too high rating"
            )
            review.full_clean()

        with self.assertRaises(ValidationError):
            review = Review(
                product=self.product,
                user=self.user,
                rating=0,
                comment="Too low rating"
            )
            review.full_clean()

    def test_str_method(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Good product"
        )
        self.assertEqual(str(review), "Review for Test Product by Test User - 4 stars")