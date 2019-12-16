import psutil
import json
import logging
import psycopg2

from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class CPUMetric:
    name = 'cpu_metric'
    machine_id: int
    user: float
    nice: float
    system: float
    idle: float
    created_at: str

    @classmethod
    def load_from_string(cls, str_value: str):
        '''Return a CPUMetric instance
        '''
        value = json.loads(str_value)
        return cls(**value)

    def dump_to_string(self):
        value = json.dumps({
            "machine_id": self.machine_id,
            "user": self.user,
            "nice": self.nice,
            "system": self.system,
            "idle": self.idle,
            "created_at": self.created_at
        })

        return value

    def save_to_db(self, connection):
        insert_str = f'INSERT INTO {self.name} \
        (machine_id, "user",nice,system,idle,created_at) \
        values (%s, %s,%s,%s,%s,%s)'

        with connection.cursor() as cur:
            try:
                cur.execute(insert_str, (self.machine_id, self.user, self.nice,
                                         self.system, self.idle, self.created_at))
                logger.info(f"inserted one metric into table: {self.name}")
            except psycopg2.Error as e:
                logger.error('Failed to insert data into table: %s', e)

        connection.commit()

    @classmethod
    def create_table(cls, connection):
        ddl = '''create table if not exists cpu_metric (
                machine_id int not null,
                "user" float,
                nice float,
                system float,
                idle float,
                created_at TIMESTAMPTZ not null);'''

        with connection.cursor() as cur:
            try:
                cur.execute(ddl)
                logger.info(f"Create table {cls.name} successfully")
            except psycopg2.Error as e:
                logger.error(f'Failed to created table {cls.name} : %s', e)

        connection.commit()


@dataclass
class MemMetric:
    name = 'mem_metric'
    machine_id: int
    total: int
    available: int
    percent: float
    used: int
    free: int
    created_at: str

    @classmethod
    def load_from_string(cls, str_value: str):
        '''Return a MemMetric instance
        '''
        value = json.loads(str_value)
        return cls(**value)

    def dump_to_string(self):
        value = json.dumps({
            "machine_id": self.machine_id,
            "total": self.total,
            "available": self.available,
            "percent": self.percent,
            "used": self.used,
            "free": self.free,
            "created_at": self.created_at
        })

        return value

    def save_to_db(self, connection):
        insert_str = f'INSERT INTO {self.name} \
            (machine_id,total,available,percent,used,free,created_at) \
            values (%s,%s,%s,%s,%s,%s,%s)'

        with connection.cursor() as cur:
            try:
                cur.execute(insert_str, (self.machine_id, self.total, self.available,
                                         self.percent, self.used, self.free, self.created_at))
                logger.info(f"inserted one metric into table: {self.name}")
            except psycopg2.Error as e:
                logger.error('Failed to insert data into table: %s', e)

        connection.commit()

    @classmethod
    def create_table(cls, connection):
        ddl = '''create table if not exists mem_metric(
                machine_id int not null,
                total bigint,
                available bigint,
                percent float,
                used bigint,
                free bigint,
                created_at TIMESTAMPTZ not null);'''

        with connection.cursor() as cur:
            try:
                cur.execute(ddl)
                logger.info(f"Create table {cls.name} successfully")
            except psycopg2.Error as e:
                logger.error(f'Failed to created table {cls.name} : %s', e)

        connection.commit()


@dataclass
class DiskMetric:
    name = 'disk_metric'
    machine_id: int
    total: int
    used: int
    free: int
    percent: float
    created_at: str

    @classmethod
    def load_from_string(cls, str_value: str):
        '''Return a DiskMetric instance
        '''
        value = json.loads(str_value)
        return cls(**value)

    def dump_to_string(self):
        value = json.dumps({
            "machine_id": self.machine_id,
            "total": self.total,
            "used": self.used,
            "free": self.free,
            "percent": self.percent,
            "created_at": self.created_at
        })

        return value

    def save_to_db(self, connection):
        insert_str = f'INSERT INTO {self.name} \
            (machine_id,total,used,free,percent,created_at) \
            values (%s,%s,%s,%s,%s,%s)'

        with connection.cursor() as cur:
            try:
                cur.execute(insert_str, (self.machine_id, self.total, self.used,
                                         self.free, self.percent, self.created_at))
                logger.info(f"inserted one metric into table: {self.name}")
            except psycopg2.Error as e:
                logger.error('Failed to insert data into table: %s', e)

        connection.commit()

    @classmethod
    def create_table(cls, connection):
        ddl = '''create table if not exists disk_metric(
                time TIMESTAMPTZ default CURRENT_TIMESTAMP,
                machine_id int,
                total bigint,
                used bigint,
                free bigint,
                percent float,
                created_at TIMESTAMPTZ not null);'''

        with connection.cursor() as cur:
            try:
                cur.execute(ddl)
                logger.info(f"Create table {cls.name} successfully")
            except psycopg2.Error as e:
                logger.error(f'Failed to created table {cls.name} : %s', e)

        connection.commit()


class SystemMonitor:
    def __init__(self, machine_id):
        '''Init a system monitor instance
        '''
        self.machine_id = machine_id

    def get_cpu_percent(self) -> CPUMetric:
        cpu = psutil.cpu_times_percent()
        return CPUMetric(self.machine_id,
                         cpu.user,
                         cpu.nice,
                         cpu.system,
                         cpu.idle,
                         datetime.now().isoformat())

    def get_memory_usage(self) -> MemMetric:
        mem = psutil.virtual_memory()
        return MemMetric(machine_id=self.machine_id,
                         total=mem.total,
                         available=mem.available,
                         percent=mem.percent,
                         used=mem.used,
                         free=mem.free,
                         created_at=datetime.now().isoformat())

    def get_disk_usage(self) -> DiskMetric:
        disk = psutil.disk_usage('/')
        return DiskMetric(machine_id=self.machine_id,
                          total=disk.total,
                          used=disk.used,
                          free=disk.free,
                          percent=disk.free,
                          created_at=datetime.now().isoformat())


def get_metrics():
    return [CPUMetric, MemMetric, DiskMetric]
