from rest_framework import serializers
from dripshop_apps.wishlist.models import Wishlist
from dripshop_apps.dripshop_account.api.v1.serializers import UserAccountSerializer
from dripshop_apps.product.api.v1.serializers import ProductSerializer

class WishlistSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = '__all__'