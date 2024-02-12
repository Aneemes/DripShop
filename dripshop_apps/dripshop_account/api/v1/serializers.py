from rest_framework import serializers
from dripshop_apps.dripshop_account.models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'