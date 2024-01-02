import uuid
from django.db import models


class FeaturedItemManager(models.Manager):
    def get_queryset(self):
        return super(FeaturedItemManager, self).get_queryset().filter(published="yes", featured="yes").order_by("-updated_date")[:10]    

class AbstractTimeStampModel(models.Model):
    """TimeStampModel that holds created_date and updated_date field"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateTimeField("Created date", auto_now_add=True)
    updated_date = models.DateTimeField("Updated date", auto_now=True)

    def __str__(self):
        return self.created_date

    class Meta:
        abstract = True

class AbstractItem(AbstractTimeStampModel):
    """AbstractItem"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)
    description = models.TextField(
        "Description",
        blank=True
    )    
    featured = models.CharField(
        verbose_name="Featured",
        max_length=3,
        default="no",
        choices=(
            ("yes", "Yes"),
            ("no", "No")
        )
    )

    published = models.CharField(
        verbose_name="published",
        max_length=3,
        default="yes",
        choices=(
            ("yes", "Yes"),
            ("no", "No")
        )
    )

    publish_timestamp = models.DateTimeField(
        # means that the publish_timestamp field will not automatically be set to the current date and time when a new instance of this model is created.
        auto_now_add=False,
        # means that the publish_timestamp field will not automatically be updated to the current date and time every time the model is saved.
        auto_now=False,
        blank=True,
        null=True
    )

    featured_objects = FeaturedItemManager()

    class Meta:
        abstract = True
    