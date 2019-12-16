import logging
import psycopg2

from app.utils.environment import Environment

logger = logging.getLogger(__name__)


class DBClient:
    def __init__(self):
        self.__conn = None

    def connect(self):
        if self.__conn:
            return self.__conn

        logger.info('Connecting database: %s', self.db_config)

        try:
            self.__conn = psycopg2.connect(**self.db_config)
            print('Connected to database:')
        except psycopg2.Error as e:
            print('Failed to connect to database:', e)
            self.__conn = None

        return self.__conn

    @property
    def connection(self):
        if self.__conn:
            return self.__conn

        environment = Environment()
        logger.info('Connecting database: %s', environment.db_config)

        try:
            self.__conn = psycopg2.connect(**environment.db_config)
            print('Connected to database:')
        except psycopg2.Error as e:
            print('Failed to connect to database:', e)
            self.__conn = None

        return self.__conn

    def __del__(self):
        print('Close DBAgent instance')
        if self.__conn:
            self.__conn.close()

    @property
    def conn(self):
        return self.__conn


dbc = DBClient()
