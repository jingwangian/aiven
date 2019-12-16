import os

from invoke import task
from app.app import start_monitor, start_etl, init_tables
from dotenv import load_dotenv
from app.utils.environment import Environment

import app


def main():
    print('This is main function')


@task
def monitor(c, prod=True):
    '''Start system monitor process

    The process will get the system all kinds of metric data and publish them into kafka
    '''
    if prod:
        load_dotenv()

    start_monitor()


@task
def etl(c, prod=True):
    '''Start etl process

    The etl process will get the data from kafka and save the result into database
    '''
    if prod:
        load_dotenv()

    start_etl()


@task()
def initdb(c, prod=True):
    if prod:
        load_dotenv()

    init_tables()


# ## uncomment this code to debug
if __name__ == "__main__":
    main()
