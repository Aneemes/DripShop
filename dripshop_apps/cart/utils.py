from dripshop_apps.cart.models import Cart
from dripshop_apps.product.models import Product
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= product.stock:
        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if new_quantity <= product.stock:
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, f"{quantity} item(s) added to your cart.")
            else:
                messages.error(request, "Requested quantity exceeds available stock.")
        else:
            Cart.objects.create(user=request.user, product=product, quantity=quantity)
            messages.success(request, f"{quantity} item(s) added to your cart.")
    else:
        messages.error(request, "Requested quantity exceeds available stock.")

    return redirect("cart:cart_detail")