from celery import shared_task
from dripshop_apps.wishlist.models import Wishlist
from celery.utils.log import get_task_logger
from dripshop_apps.product.models import Product

logger = get_task_logger(__name__)

@shared_task(name='remove_products_from_wishlist')
def remove_products_from_wishlist(user_id, product_ids):
    try:
        user_wishlist = Wishlist.objects.get(user_id=user_id)
        products_to_remove = Product.objects.filter(id__in=product_ids)
        user_wishlist.products.remove(*products_to_remove)
        return True
    except Wishlist.DoesNotExist:
        return False