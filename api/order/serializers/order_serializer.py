from django.db import transaction

from rest_framework import serializers

from api.order.models import Address, User
from api.order.models.order import Order
from api.order.serializers.user_serializer import UserSerializer
from api.order.serializers.address_serializer import AddressSerializer
from api.order.producer import send_address_to_queue


class UserOrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=True)
    user = UserSerializer(required=True)

    class Meta:
        model = Order
        fields = (
            'address',
            'user',
        )

    @transaction.atomic
    def create(self, validated_data):
        address = Address.objects.filter(street=validated_data['address']['street'])

        if address.exists():
            address_from_order = address.first()
        else:
            address_from_order = Address.objects.create(
                street=validated_data['address']['street'],
                city=validated_data['address']['city'],
                neighborhood=validated_data['address']['neighborhood'],
                zip_code=validated_data['address']['zip_code'],
                uf=validated_data['address']['uf']
            )

        user, created = User.objects.get_or_create(
            email=validated_data['user']['email'],
            name=validated_data['user']['name'],
            phone=validated_data['user']['phone'],
        )
        order = Order.objects.create(address=address_from_order, user=user)

        if not address_from_order.latitude and not address_from_order.longitude:
            send_address_to_queue(message=order.address)
        return order
