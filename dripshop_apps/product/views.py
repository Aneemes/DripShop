from .models import Product
from django.db import models
from django.views.generic import ListView, DetailView
from django.shortcuts import render, redirect
from dripshop_apps.category.models import Category
from dripshop_apps.brand.models import Brand
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from mptt.templatetags.mptt_tags import cache_tree_children
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from dripshop_apps.cart.models import Cart
from django.views import View
from django.contrib.auth.models import AnonymousUser
from dripshop_apps.wishlist.models import Wishlist

class PublishedProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.request.GET.get('category')

        queryset = Product.objects.filter(visible=True, published="yes")

        if category_id:
            category = Category.objects.get(id=category_id)
            descendant_ids = [descendant.id for descendant in cache_tree_children(category)]
            queryset = queryset.filter(category__in=descendant_ids)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.get_published()
        brands = Brand.objects.all()  # Assuming you have a model named 'Brand'

        context['categories'] = categories
        context['brands'] = brands
        context['featured_products'] = Product.objects.get_featured().filter(visible=True)
        return context

@require_GET
def update_products(request):
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    queryset = Product.objects.filter(visible=True, published="yes")

    if category_id:
        category = Category.objects.get(id=category_id)
        descendant_ids = category.get_descendants(include_self=True).values_list('id', flat=True)
        queryset = queryset.filter(category__in=descendant_ids)

    if brand_id:
        brand = Brand.objects.get(id=brand_id)
        queryset = queryset.filter(brand=brand)

    # Convert the products to a JSON format
    data = [{'title': product.title} for product in queryset]

    return JsonResponse(data, safe=False)

# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'product/product_detail.html'
#     context_object_name = 'product'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Get the user, default to None if not authenticated
#         user = self.request.user if self.request.user.is_authenticated else None
        
#         product = self.object
        
#         # Filter cart items only if the user is authenticated
#         if user:
#             cart_items = Cart.objects.filter(user=user, product=product)
#             cart_quantity = cart_items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
#             max_quantity = product.stock - cart_quantity
#             context['cart_items'] = cart_items
#             context['cart_quantity'] = cart_quantity
#             context['max_quantity'] = max_quantity
#         else:
#             context['cart_items'] = []
#             context['cart_quantity'] = 0
#             context['max_quantity'] = product.stock
        
#         context['user_authenticated'] = user.is_authenticated if user else False
#         return context


#     @method_decorator(login_required, name='post')
#     class PostView(View):
#         def post(self, request, *args, **kwargs):
#             product = self.get_object()
#             quantity = int(request.POST.get('quantity', 1))

#             cart_items = Cart.objects.filter(user=request.user, product=product)
#             cart_quantity = cart_items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
#             max_quantity = product.stock - cart_quantity

#             if quantity <= max_quantity:
#                 cart_item = cart_items.first()

#                 if cart_item:
#                     new_quantity = cart_item.quantity + quantity
#                     if new_quantity <= max_quantity:
#                         cart_item.quantity = new_quantity
#                         cart_item.save()
#                         messages.success(request, f"{quantity} item(s) added to your cart.")
#                     else:
#                         messages.error(request, "Requested quantity exceeds available stock.")
#                 else:
#                     Cart.objects.create(user=request.user, product=product, quantity=quantity)
#                     messages.success(request, f"{quantity} item(s) added to your cart.")
#             else:
#                 messages.error(request, "Requested quantity exceeds available stock.")

#             return redirect("cart:cart_detail")
    
#     # Allow unauthenticated users to view the product details
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the user, default to None if not authenticated
        user = self.request.user if self.request.user.is_authenticated else None
        
        product = self.object
        
        # Filter cart items only if the user is authenticated
        if user:
            cart_items = Cart.objects.filter(user=user, product=product)
            cart_quantity = cart_items.aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0
            max_quantity = product.stock - cart_quantity
            context['cart_items'] = cart_items
            context['cart_quantity'] = cart_quantity
            context['max_quantity'] = max_quantity
            
            # # Get the user's wishlist
            # wishlist = Wishlist.objects.filter(user=user, products=product).first()
            # context['user_wishlist'] = wishlist
            
        else:
            context['cart_items'] = []
            context['cart_quantity'] = 0
            context['max_quantity'] = product.stock
            # context['user_wishlist'] = None
        
        context['user_authenticated'] = user.is_authenticated if user else False
        return context

    @method_decorator(login_required, name='post')
    def post(self, request, *args, **kwargs):
        product = self.get_object()
        quantity = int(request.POST.get('quantity', 1))

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
    
    # Allow unauthenticated users to view the product details
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)