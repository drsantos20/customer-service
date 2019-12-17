
from rest_framework import serializers

from api.order.models.user import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=False)
    phone = serializers.IntegerField(required=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'phone')
