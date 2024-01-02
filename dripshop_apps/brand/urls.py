# dripshop_apps/category/urls.py
from django.urls import path
from .views import BrandDetailView, PublishedBrandListView

urlpatterns = [
    path('', PublishedBrandListView.as_view(), name='brand'),
    path('<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),
]
