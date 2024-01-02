from django.views.generic import TemplateView
from dripshop_apps.product.models import Product
from dripshop_apps.category.models import Category
from dripshop_apps.brand.models import Brand
from dripshop_apps.cart.models import Cart
from django.db import models
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model

class Home(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch featured products and add them to the context
        featured_products = Product.objects.get_featured().filter(visible=True)
        context['featured_products'] = featured_products

        # Fetch featured categories and add them to the context
        featured_categories = Category.objects.get_featured()
        context['featured_categories'] = featured_categories

        # Fetch featured brand and add them to the context
        featured_brands = Brand.objects.get_featured()
        context['featured_brands'] = featured_brands

        # Add cart information to the context if the user is authenticated
        if self.request.user.is_authenticated:
            User = get_user_model()
            user = User.objects.get(pk=self.request.user.pk)
            cart_items = Cart.objects.filter(user=user)
            cart_quantity = cart_items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
            context['cart_items'] = cart_items
            context['cart_quantity'] = cart_quantity

        return context
    
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Assuming 'product_id' is passed in the POST data to identify the product
        product = get_object_or_404(Product, pk=product_id)

        cart_items = Cart.objects.filter(user=request.user, product=product)
        cart_quantity = cart_items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
        max_quantity = product.stock - cart_quantity

        if quantity <= max_quantity:
            cart_item = cart_items.first()

            if cart_item:
                new_quantity = cart_item.quantity + quantity
                if new_quantity <= max_quantity:
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