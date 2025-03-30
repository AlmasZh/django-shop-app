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
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='products', null=True, blank=True)  # Allow nullable user
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

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




        """
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
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=250)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return f"{self.title} - {self.slug}"

    def get_absolute_url(self):
        return reverse('products:products_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_variations(self):
     #   Returns all variations of the product
        return self.variations.all()

    def get_main_image(self):
        return self.images.filter(is_main=True).first() or self.images.first()

class ProductVariation(models.Model):
    #Represents different variations of a product (size, color, etc.)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    
    # Variation attributes
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    season = models.CharField(max_length=100, null=True, blank=True)
    pattern = models.CharField(max_length=100, null=True, blank=True)
    origin_country = models.CharField(max_length=100, null=True, blank=True)
    
    # Price modifier (can be different from base price)
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Inventory tracking
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        # Create a descriptive string for the variation
        variation_details = []
        if self.size:
            variation_details.append(f"Size: {self.size}")
        if self.color:
            variation_details.append(f"Color: {self.color}")
        if self.season:
            variation_details.append(f"Season: {self.season}")
        
        return f"{self.product.title} - {', '.join(variation_details)}"

    def get_price(self):
        return self.product.base_price + self.price_modifier

class ProductImage(models.Model):
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='products')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        if self.variation:
            return f"{self.variation} - Image {self.id}"
        return f"{self.product.title} - Image {self.id}"
        """