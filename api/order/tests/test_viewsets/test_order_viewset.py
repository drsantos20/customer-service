import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from api.order.factories import UserOrderSerializerFactory
from api.order.models import Order, Address


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
        order = Order.objects.get(user__email='john_due@gmail.com')
        self.assertEqual(order.address.street, 'avenida paulista')
        self.assertEqual(order.address.city, 'sao paulo')
        self.assertEqual(order.address.neighborhood, 'jardim paulistano')
        self.assertEqual(order.address.zip_code, '04319-000')
        self.assertEqual(order.address.uf, 'SP')

    def test_does_not_call_address_producer_when_geo_location_is_presented(self):
        already_exist_address = Address.objects.create(
            street='avenida paulista',
            city='sao paulo',
            uf='SP',
            neighborhood='jardim paulistano',
            zip_code='04319-000',
            latitude='-23.6472437',
            longitude='-46.6368677',
        )

        data = json.dumps({
            'address': {
                'street': 'avenida paulista',
                'city': 'sao paulo',
                'uf': 'SP',
                'neighborhood': 'jardim paulistano',
                'zip_code': '04319-000'
            },
            'user': {
                'email': 'daniel_bone@gmail.com',
                'name': 'Daniel Bone',
                'phone': 999999999,
            }
        })

        response = self.client.post(
            reverse('order-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(user__email='daniel_bone@gmail.com')

        self.assertEqual(order.address.street, already_exist_address.street)
        self.assertEqual(order.address.city, already_exist_address.city)
        self.assertEqual(order.address.neighborhood, already_exist_address.neighborhood)
        self.assertEqual(order.address.zip_code, already_exist_address.zip_code)
        self.assertEqual(order.address.uf, already_exist_address.uf)
        self.assertEqual(order.address.latitude, already_exist_address.latitude)
        self.assertEqual(order.address.longitude, already_exist_address.longitude)
