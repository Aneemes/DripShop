from django.urls import include, path
from .views import PublishedProductListView, ProductDetailView, update_products

urlpatterns = [
    path('', PublishedProductListView.as_view(), name='product_list'),
    path('update_products/', update_products, name='update_products'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product_detail'),
]