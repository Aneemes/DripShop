# wishlist/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from dripshop_apps.product.models import Product

@login_required
def wishlist_add(request, product_id):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    if product not in wishlist.products.all():
        wishlist.products.add(product)

    wishlist.save()

    return redirect('product:product_detail', pk=product_id)

@login_required
def wishlist_remove(request, product_id):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)

    if product in wishlist.products.all():
        wishlist.products.remove(product)

    return redirect('product:product_detail', pk=product_id)

@login_required
def wishlist_list(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist
    }
    return render(request, 'wishlist/wishlist_list.html', context)