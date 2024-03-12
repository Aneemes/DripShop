from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm
from dripshop_apps.cart.models import Cart
from dripshop_apps.dripshop_account.models import UserAccount
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db import transaction
from dripshop_apps.order.utils import send_mail_on_order_placement, create_notification_on_order_placement
from dripshop_apps.wishlist.tasks import remove_products_from_wishlist


#order/views.py
User = get_user_model()
@login_required
def order_create(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.subtotal() for item in cart_items)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:cart_detail")

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    for cart_item in cart_items:
                        if cart_item.product.stock < cart_item.quantity:
                            # cart_items.delete() dont remove from the cart
                            messages.error(request, f"The product '{cart_item.product.title}' is out of stock. Please check back later.")
                            return redirect("cart:cart_detail")
                    
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = total_price
                    order.save()

                    for cart_item in cart_items:
                        order_item = OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

                        # Update the stock of the product
                        cart_item.product.stock -= cart_item.quantity
                        cart_item.product.save()

                    product_ids = list(order.orderitem_set.values_list('product_id', flat=True))

                    transaction.on_commit(lambda: remove_products_from_wishlist.delay(request.user.id, product_ids))     

                    cart_items.delete()

                    transaction.on_commit(lambda: send_mail_on_order_placement(request, order=order))
                    transaction.on_commit(lambda: create_notification_on_order_placement(request, order=order))

                    messages.success(request, "Your order has been placed successfully.")
                    return redirect("order:order_detail", order_id=order.id)
                
                # transaction.on_commit(order_email)

            except Exception as e:
                messages.error(request, f"There was an error placing the order: {str(e)}")

    else:
        initial_data = {
            'delivery_address': request.user.address,
            'delivery_phone': request.user.phone
        }
        form = OrderCreateForm(initial=initial_data)

    context = {
        "cart_items": cart_items,
        "form": form,
        "total_price": total_price,
    }

    return render(request, "order/order_create.html", context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        "order": order,
    }

    return render(request, "order/order_detail.html", context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(orders, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'orders': page_obj,
    }

    return render(request, 'order/order_list.html', context)