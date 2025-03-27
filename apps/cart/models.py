from django.db import models
from apps.products.models import Product
from apps.users.models import CustomUser

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        """Calculates the total price of all cart items"""
        return sum(item.total_price() for item in self.items.all())

    def total_items(self):
        """Calculates total number of items in the cart"""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart.user.username}'s cart"

    def total_price(self):
        """Returns total price of this cart item"""
        return self.quantity * self.product.price