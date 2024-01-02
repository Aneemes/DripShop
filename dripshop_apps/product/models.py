import os
from django.db import models
from dripshop_apps.core.abstract_models import AbstractItem
from dripshop_apps.category.models import Category
from dripshop_apps.brand.models import Brand
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.db.models.signals import pre_save
from dripshop_apps.core.receivers import slugify_pre_save, publish_state_pre_save, update_featured_on_publish, update_visibility_on_publish

def sanitize_for_directory_name(value):
    # Replace spaces with underscores and remove other characters
    return ''.join(c if c.isalnum() or c in ['_', '-'] else '_' for c in value)

def product_image_upload_path(instance, filename):
    print("Product instance:", instance)
    title = getattr(instance.product, 'title', 'unknown')
    print("Product title:", title)

    # Sanitize the title for directory name
    product_title = sanitize_for_directory_name(title)

    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    extension = os.path.splitext(filename)[1]
    file_path = f'uploads/products/{product_title}/general/{timestamp}{extension}'
    print("Generated Image Path:", file_path)
    return file_path

def product_thumbnail_upload_path(instance, filename):
    print("Product instance:", instance)
    title = getattr(instance, 'title', 'unknown')
    print("Product title:", title)

    # Sanitize the title for directory name
    product_title = sanitize_for_directory_name(title)
    
    timestamp = timezone.now().strftime('%Y-%m-%d_%H-%M-%S')
    extension = os.path.splitext(filename)[1]
    file_path = f'uploads/products/{product_title}/thumbnail/{timestamp}{extension}'
    print("Generated Thumbnail Path:", file_path)
    return file_path

class ProductQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published="yes")
    
    def featured(self):
        return self.filter(featured="yes")

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_published(self):
        return self.get_queryset().published()

    def get_featured(self):
        return self.get_queryset().featured()

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

