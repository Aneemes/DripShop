import os
from django.db import models
from dripshop_apps.core.abstract_models import AbstractItem
from dripshop_apps.category.models import Category
from dripshop_apps.brand.models import Brand
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from dripshop_apps.core.receivers import slugify_pre_save, publish_state_pre_save, update_featured_on_publish, update_visibility_on_publish
from .tasks import upload_to_firebase
from .utils import product_thumbnail_upload_path, product_image_upload_path, sanitize_for_directory_name



class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published="yes")
    
    def featured(self):
        return self.filter(featured="yes")

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def featured(self):
        return self.get_queryset().featured()

    def get_published(self):
        return self.published()

    def get_featured(self):
        return self.featured()

    def updated_date_string(self):
        return self.get_queryset().values_list('updated_date', flat=True).first()


class Product(AbstractItem):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,related_name='product_category', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name='product_brand', null=True, blank=True)
    thumbnail = models.ImageField(upload_to=product_thumbnail_upload_path, blank=True, null=True, max_length=255)
    visible = models.BooleanField(default=True, editable=False)
    stock = models.PositiveIntegerField(default=0)

    objects=ProductManager()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.title
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_path, blank=True, null=True, max_length=255)
    updated = models.DateTimeField(auto_now=True)
    
pre_save.connect(publish_state_pre_save, sender=Product)
pre_save.connect(slugify_pre_save, sender=Product)
pre_save.connect(update_featured_on_publish, sender=Product)
