from django.db import models
from dripshop_apps.core.abstract_models import AbstractItem
from mptt.models import MPTTModel, TreeForeignKey, MPTTOptions
from django.db.models.signals import pre_save
from dripshop_apps.core.receivers import slugify_pre_save, publish_state_pre_save, update_featured_on_publish


class CategoryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published="yes")
    
    def featured(self):
        return self.filter(featured="yes")

class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def get_published(self):
        return self.get_queryset().published()

    def get_featured(self):
        return self.get_queryset().featured()

    def updated_date_string(self):
        return self.get_queryset().values_list('updated_date', flat=True).first()

class Category(AbstractItem, MPTTModel):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='subcategories', null=True, blank=True)
    featured_products = models.ManyToManyField('product.Product', blank=True, verbose_name="Featured Products", related_name="category_featured_products")
    thumbnail = models.ImageField(        
        upload_to="uploads/thumbnail/category/%Y/%m/%d",
        max_length=255,
        blank=True,
        help_text="maximum size of thumbnail should be 255px by 300px"
    )
    objects = CategoryManager()

    def save(self, *args, **kwargs):
        # Check if the category is transitioning from unpublished to published
        transitioning_from_unpublished = self._state.adding or (Category.objects.filter(pk=self.pk, published='no').exists() and self.published == 'yes')

        # Call the parent class's save method
        super().save(*args, **kwargs)

        # Update visibility status of related products based on the publishing status of the category
        if transitioning_from_unpublished:
            self.product_category.update(visible=True)
        elif self.published == 'no':
            self.product_category.update(visible=False)
        else:
            self.product_category.update(visible=True)

    def __str__(self):
        return self.title

    class MPTTMeta(MPTTOptions):
        order_insertion_by = ['title']
        verbose_name = "category"
        verbose_name_plural = "categories"

pre_save.connect(publish_state_pre_save, sender=Category)
pre_save.connect(slugify_pre_save, sender=Category)
pre_save.connect(update_featured_on_publish, sender=Category)
