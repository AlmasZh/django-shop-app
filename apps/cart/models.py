from django.db import models
from apps.products.models import Product
from apps.users.models import CustomUser

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.first_name} {self.user.last_name}"

    def total_price(self):
        """Calculates the total price of all cart items"""
        return sum(item.total_price() for item in self.items.all())

    def total_items(self):
        """Calculates total number of items in the cart"""
        return sum(item.quantity for item in self.items.all())
    
    def add_product(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            cart=self, 
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item

    def remove_product(self, product):
        CartItem.objects.filter(cart=self, product=product).delete()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.cart.user.first_name} {self.cart.user.last_name}'s cart"

    def total_price(self):
        """Returns total price of this cart item"""
        return self.quantity * self.product.price
    
    def update_quantity(self, new_quantity):
        """
        Update the quantity of this cart item
        """
        if new_quantity < 1:
            self.delete()
        else:
            self.quantity = new_quantity
            self.save()