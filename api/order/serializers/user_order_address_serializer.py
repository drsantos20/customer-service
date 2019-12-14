from rest_framework import serializers

from api.order.models.address import UserOrderAddress


class UserOrderAddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    neighborhood = serializers.CharField(required=False)
    zip_code = serializers.CharField(required=False)
    uf = serializers.CharField(required=False)

    class Meta:
        model = UserOrderAddress
        fields = (
            'street',
            'city',
            'neighborhood',
            'zip_code',
            'uf',
        )
