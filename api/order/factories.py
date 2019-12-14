import factory

from api.order.models import UserOrderAddress


class UserOrderAddressFactory(factory.DjangoModelFactory):
    street = factory.Faker('pystr')
    city = factory.Faker('pystr')
    neighborhood = factory.Faker('pystr')
    zip_code = factory.Faker('pystr')
    uf = factory.Faker('pystr')

    class Meta:
        model = UserOrderAddress
