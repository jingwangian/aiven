import logging

# from collections import defaultdict
from kafka import KafkaProducer
from kafka import KafkaConsumer

from app.utils.environment import Environment

logger = logging.getLogger(__name__)


class ProducerError(Exception):
    pass


class Producer:
    def __init__(self, topic_name: str):
        '''Init a producer instance
        '''
        self.topic_name = topic_name
        self.producer = None

    def connect(self):
        '''Connect to Kafka service
        '''
        environment = Environment()

        logger.info('environment = %s', environment)

        try:
            host_addr = f'{environment.KAFKA_HOST}:{environment.KAFKA_PORT}'
            logger.info(f'Connecting to kafka at {host_addr}')
            self.producer = KafkaProducer(
                bootstrap_servers=[host_addr],
                ssl_keyfile=environment.KAFKA_SSL_KEYFILE,
                ssl_cafile=environment.KAFKA_SSL_CAFILE,
                ssl_certfile=environment.KAFKA_SSL_CERTFILE,
                security_protocol=environment.KAFKA_SSL_PROTOCOL)

        except Exception as ex:
            logger.error('Exception while connecting Kafka: %s', ex)
            # print(str(ex))
            self.producer = None
            raise ProducerError('Failed to connect to kafka')

    def publish_message(self, key: str, value: str):
        '''Publish the message to kafka
        '''
        producer_instance = self.producer
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            producer_instance.send(self.topic_name, key=key_bytes, value=value_bytes)
            producer_instance.flush()
            logger.info(f'Message with key {key} published to {self.topic_name} successfully.')
        except Exception as ex:
            logger.error(f'Exception in publishing message with key {key} to {self.topic_name}: %s', ex)
            raise ex


class Consumer:
    @classmethod
    def get_consumer(cls):
        '''Generate a consumer instance
        '''
        environment = Environment()
        host_addr = f'{environment.KAFKA_HOST}:{environment.KAFKA_PORT}'
        consumer = KafkaConsumer(environment.KAFKA_TOPIC,
                                 bootstrap_servers=host_addr,
                                 ssl_keyfile=environment.KAFKA_SSL_KEYFILE,
                                 ssl_cafile=environment.KAFKA_SSL_CAFILE,
                                 ssl_certfile=environment.KAFKA_SSL_CERTFILE,
                                 security_protocol=environment.KAFKA_SSL_PROTOCOL)
        return consumer
