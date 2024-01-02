from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart
from dripshop_apps.product.models import Product
from django.db.models import F

# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     quantity = int(request.POST.get('quantity', 1))

#     if quantity <= product.stock:
#         cart_item = Cart.objects.filter(user=request.user, product=product).first()

#         if cart_item:
#             new_quantity = cart_item.quantity + quantity
#             if new_quantity <= product.stock:
#                 cart_item.quantity = new_quantity
#                 cart_item.save()
#                 messages.success(request, f"{quantity} item(s) added to your cart.")
#             else:
#                 messages.error(request, "Requested quantity exceeds available stock.")
#         else:
#             Cart.objects.create(user=request.user, product=product, quantity=quantity)
#             messages.success(request, f"{quantity} item(s) added to your cart.")
#     else:
#         messages.error(request, "Requested quantity exceeds available stock.")

#     return redirect("cart:cart_detail")

from .utils import add_to_cart

@login_required
def cart_add(request, product_id):
    return add_to_cart(request, product_id)

@login_required
def update_quantity(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    if cart_item.user == request.user:
        if request.method == 'POST':
            action = request.POST.get('action')

            if action == 'subtract':
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
            elif action == 'add':
                new_quantity = cart_item.quantity + 1
                if new_quantity <= cart_item.product.stock:
                    cart_item.quantity = new_quantity

            cart_item.save()
            messages.success(request, "Quantity updated.")

    return redirect("cart:cart_detail")

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")

    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum(item.subtotal() for item in cart_items)

    context = {
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "cart/cart_detail.html", context)