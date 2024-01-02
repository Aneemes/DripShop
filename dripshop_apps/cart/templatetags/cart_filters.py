# cart/templatetags/cart_filters.py
from django import template
from dripshop_apps.cart.models import Cart

register = template.Library()

@register.filter(name='get_cart_item')
def get_cart_item(product, user):
    if user.is_authenticated:
        cart_item = Cart.objects.filter(user=user, product=product).first()
        return cart_item
    else:
        return None
