from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from dripshop_apps.product.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def subtotal(self):
        return self.quantity * self.product.price
