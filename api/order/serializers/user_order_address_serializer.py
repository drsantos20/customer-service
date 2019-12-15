from django.db import transaction
from rest_framework import serializers

from api.order.models.address import UserOrderAddress
from api.order.tasks import publish_metadata


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

    @transaction.atomic
    def create(self, validated_data):
        user_address = UserOrderAddress.objects.create(
            street=validated_data['street'],
            city=validated_data['city'],
            neighborhood=validated_data['neighborhood'],
            zip_code=validated_data['zip_code'],
            uf=validated_data['uf']
        )
        publish_metadata(message=user_address.id)

        return user_address
