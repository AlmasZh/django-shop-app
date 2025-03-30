from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
        ('unisex', 'Unisex'),
    ]

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='unisex',
        blank=True,
    )

    title = models.CharField(max_length=250)
    brand_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    season = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    pattern = models.CharField(max_length=100, null=True, blank=True)
    origin_country = models.CharField(max_length=100, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"{self.title} - {self.slug}"

    def get_absolute_url(self):
        return reverse('products:products_detail', kwargs={'slug':self.slug})
    
    def get_main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.title} - {self.id}"