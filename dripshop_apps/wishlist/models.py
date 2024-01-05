# wishlist/models.py
from django.db import models
from django.contrib.auth import get_user_model
from dripshop_apps.product.models import Product

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist for {self.user.username}"
