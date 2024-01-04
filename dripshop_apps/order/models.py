from django.db import models
from django.contrib.auth.models import User
from dripshop_apps.product.models import Product
from django.conf import settings
from django.urls import reverse

import base58
import random
import string

def generate_alphanumeric_id(length=8):
    # Generate a random alphanumeric ID
    alphanumeric_id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))

    return alphanumeric_id

# class Base58OrderIDField(models.BigIntegerField):
#     def to_python(self, value):
#         return super().to_python(value)

#     def from_db_value(self, value, expression, connection):
#         return super().from_db_value(value, expression, connection)

#     def get_db_prep_save(self, value, connection):
#         return super().get_db_prep_save(value, connection)
    
#     def pre_save(self, model_instance, add):
#         value = getattr(model_instance, self.attname)
#         if value is None:
#             value = generate_base58_id()  # Replace this with your actual ID generation logic
#             setattr(model_instance, self.attname, value)
#         return value

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.CharField(max_length=10, primary_key=True, default=generate_alphanumeric_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_address = models.CharField(max_length=255)
    delivery_phone = models.CharField(max_length=10)

    def __str__(self):
        return f"Order {self.id}"

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.pk,))

    def get_absolute_url(self):
        return reverse("order:order_detail", args=(self.id,))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price