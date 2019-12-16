"""This is a helper module to get all settings"""
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Environment(metaclass=Singleton):
    def __init__(self):
        self.config_file_name = None
        self.config = None

        self.db_config = {
            'host': os.getenv('PGDB_HOST', 'localhost'),
            'port': os.getenv('PGDB_PORT', 5432),
            'dbname': os.getenv('PGDB_DB', 'postgres'),
            'user': os.getenv('PGDB_USER', 'postgres'),
            'password': os.getenv('PGDB_PASSWORD', 'aiven2019testpass'),
            'sslmode': os.getenv('PGDB_SSLMODE', 'disable')
        }

        self.KAFKA_HOST = os.getenv('KAFKA_HOST', 'localhost')
        self.KAFKA_PORT = os.getenv('KAFKA_PORT', 29092)
        self.KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'test')
        self.KAFKA_SSL_KEYFILE = os.getenv('KAFKA_SSL_KEYFILE', None)
        self.KAFKA_SSL_CERTFILE = os.getenv('KAFKA_SSL_CERTFILE', None)
        self.KAFKA_SSL_CAFILE = os.getenv('KAFKA_SSL_CAFILE', None)
        self.KAFKA_SSL_PROTOCOL = os.getenv('KAFKA_SSL_PROTOCOL', 'PLAINTEXT')

        self.MACHINE_ID = os.getenv('MACHINE_ID', '123')
        self.MONITOR_PERIOD = os.getenv('MONITOR_PERIOD', 2)
