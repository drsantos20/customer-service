from django.conf import settings
from kombu import Connection, Exchange, Producer, Queue


def publish_metadata(message):
    connection = Connection(settings.BROKER_URL)
    connection.connect()
    channel = connection.channel()

    exchange = Exchange('example-exchange', type='direct')

    producer = Producer(
        channel=channel,
        routing_key='address',
        exchange=exchange,
    )
    queue = Queue(
        name='order-customer-queue',
        routing_key='address',
        exchange=exchange,
    )

    from api.order.serializers import UserOrderAddressSerializer
    address_serializer = UserOrderAddressSerializer(message).data

    queue.maybe_bind(connection)
    queue.declare()
    producer.publish(address_serializer)
    connection.close()


def process_address(message):
    from api.order.models import UserOrderAddress
    address = UserOrderAddress.objects.get(id=message.get('id'))
    address.latitude = message.get('lat')
    address.longitude = message.get('lng')
    address.save()
