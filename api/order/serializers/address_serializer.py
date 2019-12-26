from django.db import transaction
from rest_framework import serializers

from api.order.models.address import Address
from api.order.producer import send_address_to_queue


class AddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    neighborhood = serializers.CharField(required=False)
    zip_code = serializers.CharField(required=False)
    uf = serializers.CharField(required=False)

    class Meta:
        model = Address
        fields = (
            'id',
            'street',
            'city',
            'neighborhood',
            'zip_code',
            'uf',
        )

    @transaction.atomic
    def create(self, validated_data):
        address = Address.objects.filter(street=validated_data['address']['street'])

        if address.exists():
            user_address = address.first()
        else:
            user_address = Address.objects.create(
                street=validated_data['street'],
                city=validated_data['city'],
                neighborhood=validated_data['neighborhood'],
                zip_code=validated_data['zip_code'],
                uf=validated_data['uf']
            )
        if not user_address.latitude and not user_address.longitude:
            send_address_to_queue(message=user_address.id)

        return user_address
