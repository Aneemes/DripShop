from rest_framework import serializers
from dripshop_apps.order.models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'