from celery.utils.log import get_task_logger
from django.conf import settings
from kombu import Connection, Exchange, Producer, Queue

from api.order.constants import (
    ADDRESS_EXCHANGE,
    ADDRESS_PRODUCER_ROUTING_KEY,
    ADDRESS_PRODUCER_QUEUE,
)


logger = get_task_logger(__name__)


def send_address_to_queue(message):
    logger.info('Starting to send a message to {} queue'.format(ADDRESS_PRODUCER_QUEUE))
    with Connection(settings.BROKER_URL) as connection:
        logger.info('Connected into the broker with success')
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

        from api.order.serializers import AddressSerializer
        address_serializer = AddressSerializer(message).data

        queue.maybe_bind(connection)
        queue.declare()
        producer.publish(address_serializer)
        connection.close()
