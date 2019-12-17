import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from api.order.factories import UserOrderSerializerFactory
from api.order.models import UserOrder


class TestUserOrderAddressViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.order = UserOrderSerializerFactory()

    def test_get_all_order(self):
        response = self.client.get(
            reverse('order-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order_response_data = json.loads(response.content)

        self.assertEqual(order_response_data[0]['address']['street'], self.order.address.street)
        self.assertEqual(order_response_data[0]['address']['city'], self.order.address.city)
        self.assertEqual(order_response_data[0]['address']['uf'], self.order.address.uf)
        self.assertEqual(order_response_data[0]['address']['neighborhood'], self.order.address.neighborhood)
        self.assertEqual(order_response_data[0]['address']['zip_code'], self.order.address.zip_code)
        self.assertEqual(order_response_data[0]['user']['email'], self.order.user.email)

    def test_create_new_order(self):
        data = json.dumps({
            'address': {
                'street': 'avenida paulista',
                'city': 'sao paulo',
                'uf': 'SP',
                'neighborhood': 'jardim paulistano',
                'zip_code': '04319-000'
            },
            'user': {
                'email': 'john_due@gmail.com',
                'name': 'John',
                'phone': 999999999,
            }
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = UserOrder.objects.get(user__email='john_due@gmail.com')
        self.assertEqual(order.address.street, 'avenida paulista')
        self.assertEqual(order.address.city, 'sao paulo')
        self.assertEqual(order.address.neighborhood, 'jardim paulistano')
        self.assertEqual(order.address.zip_code, '04319-000')
        self.assertEqual(order.address.uf, 'SP')

