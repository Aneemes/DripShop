from .views import wishlist_add, wishlist_remove, wishlist_list
from django.urls import path

urlpatterns = [
    path('', wishlist_list, name='wishlist_list'),
    path('add/<uuid:product_id>/', wishlist_add, name='wishlist_add'),
    path('remove/<uuid:product_id>/', wishlist_remove, name='wishlist_remove'),
]