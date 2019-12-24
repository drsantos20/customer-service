import factory

from api.order.models import UserOrderAddress
from api.order.models.user import User
from api.order.models.order import UserOrder


class UserOrderAddressFactory(factory.DjangoModelFactory):
    street = factory.Faker('pystr')
    city = factory.Faker('pystr')
    neighborhood = factory.Faker('pystr')
    latitude = factory.Faker('pystr')
    longitude = factory.Faker('pystr')

    class Meta:
        model = UserOrderAddress


class UserFactory(factory.DjangoModelFactory):
    name = factory.Faker('pystr')
    email = factory.Faker('pystr')
    phone = factory.Faker('pyint')

    class Meta:
        model = User


class UserOrderSerializerFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    address = factory.SubFactory(UserOrderAddressFactory)

    class Meta:
        model = UserOrder
