from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("add/<uuid:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:cart_item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('update_quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
]
