from django.test import TestCase

from api.order.factories import UserOrderSerializerFactory
from api.order.serializers.order_serializer import UserOrderSerializer


class TestUserOrderSerializer(TestCase):
    def setUp(self):
        self.order = UserOrderSerializerFactory()
        self.order_serializer = UserOrderSerializer(instance=self.order)

    def test_get_order_serializer(self):
        serializer_data = self.order_serializer.data

        self.assertEqual(serializer_data['address']['street'], self.order.address.street)
        self.assertEqual(serializer_data['address']['city'], self.order.address.city)
        self.assertEqual(serializer_data['address']['uf'], self.order.address.uf)
        self.assertEqual(serializer_data['address']['neighborhood'], self.order.address.neighborhood)
        self.assertEqual(serializer_data['address']['zip_code'], self.order.address.zip_code)

        self.assertEqual(serializer_data['user']['email'], self.order.user.email)
        self.assertEqual(serializer_data['user']['name'], self.order.user.name)
        self.assertEqual(serializer_data['user']['phone'], self.order.user.phone)
