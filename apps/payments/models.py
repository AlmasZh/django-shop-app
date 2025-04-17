from django.db import models
from apps.users.models import CustomUser
from apps.orders.models import Order

# Create your models here.

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)

class BillingAddress(models.Model):
    user = models.ForeignKey(CustomUser,
                            on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100, null=True, blank=True)
    apartment_address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=100, null=True, blank=True)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES, default='B')
    # default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = 'BillingAddresses'


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(CustomUser,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.user.email

# class Refund(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     reason = models.TextField()
#     accepted = models.BooleanField(default=False)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.pk}"
