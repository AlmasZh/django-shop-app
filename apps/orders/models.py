from django.db import models
from apps.users.models import CustomUser
from apps.products.models import Product

# Create your models here.
class Order(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    payment = models.ForeignKey(
        'payments.Payment', on_delete=models.SET_NULL, blank=True, null=True)
    billing_address = models.ForeignKey(
        'payments.BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    shipping_address = models.ForeignKey(
        'payments.BillingAddress', on_delete=models.SET_NULL, blank=True, null=True, related_name='shipping_orders'
    )
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - order id: {self.id}"

    @property
    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.product.price * self.quantity


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.DELIVERY_STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def get_status_display(self):
        return dict(Order.DELIVERY_STATUS_CHOICES)[self.status]