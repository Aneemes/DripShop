from rest_framework import serializers
from dripshop_apps.product.models import(
    Product,
    ProductImage,
)
from dripshop_apps.category.api.v1.serializers import CategorySerializer
from dripshop_apps.brand.api.v1.serializers import BrandSerializer

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelField):
    category = CategorySerializer()
    brand = BrandSerializer()
    productimage_set = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'