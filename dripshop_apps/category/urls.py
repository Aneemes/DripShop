# dripshop_apps/category/urls.py
from django.urls import path
from .views import CategoryDetailView, PublishedCategoryListView

urlpatterns = [
    path('', PublishedCategoryListView.as_view(), name='category'),
    path('<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
]
