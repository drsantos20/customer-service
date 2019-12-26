from django.test import TestCase

from api.order.factories import UserOrderAddressFactory
from api.order.serializers.address_serializer import AddressSerializer


class TestUserOrderAddressSerializer(TestCase):
    def setUp(self):
        self.address = UserOrderAddressFactory(
            street='avenida faria lima',
            city='sao paulo',
            uf='SP',
            neighborhood='jardim paulistano',
            zip_code='01451-912',
        )

        self.address_serializer = AddressSerializer(instance=self.address)

    def test_get_address_serializer(self):
        serializer_data = self.address_serializer.data

        self.assertEqual(serializer_data['street'], 'avenida faria lima')
        self.assertEqual(serializer_data['city'], 'sao paulo')
        self.assertEqual(serializer_data['uf'], 'SP')
        self.assertEqual(serializer_data['neighborhood'], 'jardim paulistano')
        self.assertEqual(serializer_data['zip_code'], '01451-912')
