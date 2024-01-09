from celery import shared_task

@shared_task(name='update_category_related_product_visibility')
def update_related_product_visibility(category_id, published):
    # Import necessary models here
    from dripshop_apps.category.models import Category

    category = Category.objects.get(pk=category_id)
    products = category.product_category.all()

    # Update visibility status of related products based on the publishing status of the category
    for product in products:
        if published:
            product.visible = True
        else:
            product.visible = category.published == 'yes'
        product.save()