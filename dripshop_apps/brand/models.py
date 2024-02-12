from django.db import models
from dripshop_apps.core.abstract_models import AbstractItem
from django.db.models.signals import pre_save
from dripshop_apps.core.receivers import slugify_pre_save, publish_state_pre_save, update_featured_on_publish

class BrandQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published="yes")
    
    def featured(self):
        return self.filter(featured="yes")

class BrandManager(models.Manager):
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db)

    def get_published(self):
        return self.get_queryset().published()

    def get_featured(self):
        return self.get_queryset().featured()

    def updated_date_string(self):
        return self.get_queryset().values_list('updated_date', flat=True).first()
    
class Brand(AbstractItem):
    featured_products = models.ManyToManyField('product.Product', blank=True, verbose_name="Featured Products", related_name="brand_featured_products")
    logo = models.ImageField(        
        upload_to="uploads/logo/brand/%Y/%m/%d",
        max_length=255,
        blank=True,
        help_text="maximum size of logo should be 255px by 300px"
    )
    objects = BrandManager()

    def save(self, *args, **kwargs):
        # Check if the brand is transitioning from unpublished to published
        transitioning_from_unpublished = self._state.adding or (Brand.objects.filter(pk=self.pk, published='no').exists() and self.published == 'yes')

        # Call the parent class's save method
        super().save(*args, **kwargs)

        # Update visibility status of related products based on the publishing status of the brand
        if transitioning_from_unpublished:
            self.product_brand.update(visible=True)
        elif self.published == 'no':
            self.product_brand.update(visible=False)
        else:
            self.product_brand.update(visible=True)

    def get_item_count(self):
        item_count = self.product_brand.count()
        return item_count

    def __str__(self):
        return self.title

    class Meta:
        # ordering = ("title",)
        verbose_name = "brand"
        verbose_name_plural = "brands"

pre_save.connect(publish_state_pre_save, sender=Brand)
pre_save.connect(slugify_pre_save, sender=Brand)
pre_save.connect(update_featured_on_publish, sender=Brand)
