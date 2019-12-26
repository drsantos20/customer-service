import json

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from django.urls import reverse

from api.order.factories import UserOrderAddressFactory
from api.order.models import Address


class TestUserOrderAddressViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.address = UserOrderAddressFactory(
            street='avenida faria lima',
            city='sao paulo',
            uf='SP',
            neighborhood='jardim paulistano',
            zip_code='01451-912',
        )

    def test_get_all_address(self):
        response = self.client.get(
            reverse('address-list', kwargs={'version': 'v1'})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address_response_data = json.loads(response.content)

        self.assertEqual(address_response_data[0]['street'], self.address.street)
        self.assertEqual(address_response_data[0]['city'], self.address.city)
        self.assertEqual(address_response_data[0]['uf'], self.address.uf)
        self.assertEqual(address_response_data[0]['neighborhood'], self.address.neighborhood)
        self.assertEqual(address_response_data[0]['zip_code'], self.address.zip_code)

    def test_create_new_address(self):
        data = json.dumps({
            'street': 'avenida paulista',
            'city': 'sao paulo',
            'uf': 'SP',
            'neighborhood': 'jardim paulistano',
            'zip_code': '04319-000'
        })

        response = self.client.post(
            reverse('address-list', kwargs={'version': 'v1'}),
            data=data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        address = Address.objects.get(street='avenida paulista')

        self.assertEqual(address.street, 'avenida paulista')
        self.assertEqual(address.city, 'sao paulo')
        self.assertEqual(address.uf, 'SP')
        self.assertEqual(address.neighborhood, 'jardim paulistano')
        self.assertEqual(address.zip_code, '04319-000')
