from rest_framework import serializers
from dripshop_apps.brand.models import Brand

class BrandSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='get_item_count', read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'