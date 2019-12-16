import time
import logging

from app.monitor.monitor import SystemMonitor
from app.monitor import monitor
from app.utils.pubsub import Producer, Consumer
from app.utils.environment import Environment
from app import db

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


def start_monitor():
    '''start the monitor process
    '''
    logger.info('Enter start_monitor')
    environment = Environment()

    sys_monitor = SystemMonitor(environment.MACHINE_ID)

    try:
        producer = Producer(environment.KAFKA_TOPIC)
        producer.connect()
    except Exception as e:
        logger.error('Failed to create producer:%s', e)
        return

    period_time = environment.MONITOR_PERIOD

    while True:
        cpu_metric = sys_monitor.get_cpu_percent()
        value = cpu_metric.dump_to_string()
        producer.publish_message(cpu_metric.name, value)

        mem_metric = sys_monitor.get_memory_usage()
        value = mem_metric.dump_to_string()
        producer.publish_message(mem_metric.name, value)

        disk_metric = sys_monitor.get_disk_usage()
        value = disk_metric.dump_to_string()
        producer.publish_message(disk_metric.name, value)

        time.sleep(period_time)


def start_etl():
    '''start the etl process
    '''
    logger.info('Enter start_etl function')
    connection = db.dbc.connection

    if not connection:
        logger.error('Failed to get connection to database')
        return

    consumer = Consumer.get_consumer()

    # dict to store the key and the message handler function
    message_mapping = {m.name: m.load_from_string for m in monitor.get_metrics()}

    for record in consumer:
        print(record)
        key = record.key.decode()

        # Get the corresponding message handler function
        f = message_mapping.get(key)

        if f:
            value = record.value.decode()
            metric = f(value)
            logger.info(metric)

            # Any exceptin happened here will exit the loop
            metric.save_to_db(connection)


def init_tables():
    connection = db.dbc.connection

    if not connection:
        logger.error('Failed to get connection to database')
        return

    for metric in monitor.get_metrics():
        metric.create_table(connection)
