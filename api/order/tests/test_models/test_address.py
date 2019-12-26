from django.test import TestCase

from api.order.factories import UserOrderAddressFactory
from api.order.models import Address


class UserOrderAddressTestCase(TestCase):
    def setUp(self):
        self.address = UserOrderAddressFactory()

    def test_get_saved_model_address(self):
        address_from_database = Address.objects.get(id=self.address.id)
        self.assertEqual(self.address.street, address_from_database.street)
        self.assertEqual(self.address.city, address_from_database.city)
        self.assertEqual(self.address.neighborhood, address_from_database.neighborhood)
        self.assertEqual(self.address.zip_code, address_from_database.zip_code)
        self.assertEqual(self.address.uf, address_from_database.uf)
