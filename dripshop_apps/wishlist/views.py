# wishlist/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from dripshop_apps.product.models import Product
from django.urls import reverse

@login_required
def wishlist_add(request, product_id):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    if product not in wishlist.products.all():
        wishlist.products.add(product)

    wishlist.save()

    # Redirect back to the current page
    return redirect(request.META.get('HTTP_REFERER', reverse('product:product_list')))

@login_required
def wishlist_remove(request, product_id):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    if product in wishlist.products.all():
        wishlist.products.remove(product)

    # Redirect back to the current page
    return redirect(request.META.get('HTTP_REFERER', reverse('product:product_list')))

@login_required
def wishlist_list(request):
    wishlist = Wishlist.objects.filter(user=request.user, products__visible=True)
    context = {
        'wishlist': wishlist
    }
    return render(request, 'wishlist/wishlist_list.html', context)