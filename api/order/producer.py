from django.conf import settings
from kombu import Connection, Exchange, Producer, Queue

from api.order.constants import (
    ADDRESS_EXCHANGE,
    ADDRESS_PRODUCER_ROUTING_KEY,
    ADDRESS_PRODUCER_QUEUE,
)


def send_address_to_queue(message):
    with Connection(settings.BROKER_URL) as connection:
        connection.connect()
        channel = connection.channel()

        exchange = Exchange(ADDRESS_EXCHANGE, type='direct')

        producer = Producer(
            channel=channel,
            routing_key=ADDRESS_PRODUCER_ROUTING_KEY,
            exchange=exchange,
        )
        queue = Queue(
            name=ADDRESS_PRODUCER_QUEUE,
            routing_key=ADDRESS_PRODUCER_ROUTING_KEY,
            exchange=exchange,
        )

        from api.order.serializers import UserOrderAddressSerializer
        address_serializer = UserOrderAddressSerializer(message).data

        queue.maybe_bind(connection)
        queue.declare()
        producer.publish(address_serializer)
        connection.close()
