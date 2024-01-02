from django.utils import timezone
from django.utils.text import slugify

def publish_state_pre_save(sender, instance, **kwargs):
    is_publish = instance.published == "yes"
    is_draft = instance.published == "no"

    if is_publish and instance.publish_timestamp is None:
        instance.publish_timestamp = timezone.now()
    elif is_draft:
        instance.publish_timestamp = None

def slugify_pre_save(sender, instance, **kwargs):
    name = instance.title
    slug = instance.slug
    if slug is None:
        instance.slug = slugify(name)

def update_featured_on_publish(instance, **kwargs):
    # If the category is published as 'no', set featured to 'no'
    if instance.published == 'no':
        instance.featured = 'no'

def update_visibility_on_publish(instance, **kwargs):
    # If the category is unpublished, set product's featured to 'no' and visibility to False
    if instance.category and instance.category.published == 'no':
        instance.featured = 'no'
        instance.visible = False
    else:
        # If the category is published, set visibility to True
        instance.visible = True
