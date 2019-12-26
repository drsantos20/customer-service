from django.test import TestCase

from api.order.factories import UserOrderSerializerFactory
from api.order.models.order import Order


class UserOrderAddressTestCase(TestCase):
    def setUp(self):
        self.order = UserOrderSerializerFactory()

    def test_get_saved_model_order(self):
        order_from_database = Order.objects.get(id=self.order.id)
        self.assertEqual(self.order.id, order_from_database.id)
        self.assertEqual(self.order.address.street, order_from_database.address.street)
        self.assertEqual(self.order.address.city, order_from_database.address.city)
        self.assertEqual(self.order.address.neighborhood, order_from_database.address.neighborhood)
        self.assertEqual(self.order.address.zip_code, order_from_database.address.zip_code)
        self.assertEqual(self.order.address.uf, order_from_database.address.uf)
