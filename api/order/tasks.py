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
    )

    queue.maybe_bind(connection)
    queue.declare()
    producer.publish(message)
