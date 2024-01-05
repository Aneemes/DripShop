from celery import shared_task
from dripshop_apps.wishlist.models import Wishlist
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name='send_email_task')
def remove_products_from_wishlist(user_id, product_ids):
    try:
        user_wishlist = Wishlist.objects.get(user_id=user_id)
        user_wishlist.products.remove(*product_ids)
        return True
    except Wishlist.DoesNotExist:
        return False