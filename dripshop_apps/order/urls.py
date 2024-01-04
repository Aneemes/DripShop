# order/urls.py
from django.urls import path
from .views import order_create, order_detail, order_list

app_name = 'order'

urlpatterns = [
    path("create/", order_create, name="order_create"),
    # path("confirmation/", order_confirmation, name="order_confirmation"),
    path("order/<str:order_id>/", order_detail, name="order_detail"),
    path('list/', order_list, name='order_list'),
]
