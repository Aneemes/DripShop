from rest_framework import serializers
from dripshop_apps.category.models import Category

class CategorySerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source='get_item_count', read_only=True)

    class Meta:
        model = 'Category'
        fields = '__all__'