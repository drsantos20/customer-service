from celery.utils.log import get_task_logger

from django.conf import settings
from kombu import Connection, Exchange, Queue, Consumer
import socket
from api.celery import app
from api.order.utils import update_address
from api.order.constants import (
    ADDRESS_EXCHANGE,
    ADDRESS_CONSUMER_ROUTING_KEY,
    ADDRESS_CONSUMER_QUEUE
)

logger = get_task_logger(__name__)


@app.task
def consumer_from_queue():
    connection = Connection(settings.BROKER_URL, heartbeat=10)
    connection.connect()

    exchange = Exchange(ADDRESS_EXCHANGE, type='direct')

    queue = Queue(
        name=ADDRESS_CONSUMER_QUEUE,
        routing_key=ADDRESS_CONSUMER_ROUTING_KEY,
        exchange=exchange,
    )

    def process_message(body, message):
        logger.info('Message arrived with the following body {}'.format(body))
        update_address(body)
        message.ack()

    consumer = Consumer(connection, queues=queue, callbacks=[process_message], accept=['json', 'pickle', 'msgpack'])
    consumer.consume()

    def establish_connection():
        revived_connection = connection.clone()
        revived_connection.ensure_connection(max_retries=3)
        channel = revived_connection.channel()
        consumer.revive(channel)
        consumer.consume()
        return revived_connection

    def consume():
        new_connection = establish_connection()
        while True:
            try:
                new_connection.drain_events(timeout=2)
            except socket.timeout:
                new_connection.heartbeat_check()

    def run():
        logger.info('Starting consumer from address queue')
        while True:
            try:
                consume()
            except connection.connection_errors:
                logger.error('Something went wrong')
            finally:
                connection.close()

    run()


consumer_from_queue.delay()
