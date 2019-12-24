from django.db import transaction

from rest_framework import serializers

from api.order.models import UserOrderAddress, User
from api.order.models.order import UserOrder
from api.order.serializers.user_serializer import UserSerializer
from api.order.serializers.user_order_address_serializer import UserOrderAddressSerializer
from api.order.tasks import publish_metadata


class UserOrderSerializer(serializers.ModelSerializer):
    address = UserOrderAddressSerializer(required=True)
    user = UserSerializer(required=True)

    class Meta:
        model = UserOrder
        fields = (
            'address',
            'user',
        )

    @transaction.atomic
    def create(self, validated_data):
        address = UserOrderAddress.objects.filter(street=validated_data['address']['street'])

        if address.exists():
            address_from_order = address.first()
        else:
            address_from_order = UserOrderAddress.objects.create(
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
        order = UserOrder.objects.create(address=address_from_order, user=user)

        if not address_from_order.latitude and not address_from_order.longitude:
            publish_metadata(message=order.address)
        return order
