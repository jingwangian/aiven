# Small monitor system

## Introduce
This is a small system that generates system metrics and passes the events through the Kafka instance to the PostgreSQL database.

### There are different components for this system:
---
#### SystemMonitor: 
generate the all kinds of metrics instance

#### Producer:
Provide a way to publish the message to Kafka

#### Consumer: 
Provide a way to get the message from Kafak

#### dbc: 
Provide a connection to PostgreSQL database

#### Metric Class:
1. Encode the message before send it to kafka.
2. Decode the message from kafka and provide an interface to save into the database

#### start_etl:
Start the etl process which get the message from kafka and save into database

#### start_monitor:
Start the monitor process which create the metric and publish them into kafka

## Prerequisite
---
Install the [docker](https://docs.docker.com/v17.09/engine/installation/)

Install the [docker-compose](https://docs.docker.com/compose/install/)

## Init 
---
1. Create the images:

    ```
    make build
    ```

2. Set the .env file<br>
    .env file will contains the security information that let the system can connect to the kafka and database. 

    The file normally should not be saved into the repo.
For the test purpose it saved into the repo to let the tester people can use it conveniently.

3. create the tables in database(if not exists)

    ```
    make initdb
    ```


## Start the monitor and etl
---

1. start the etl process

    ```
    make etl
    ```

2. start the monitor process

    ```
    make monitor
    ```


## Using local kakfa/database
---
If you want to test it by using the local kakfa and pg-db, then run the following commands:

#### Start the database and kafka:

```bash
docker-compose up -d pg-db zookeeper kafka
```


#### Set the topic

```
./scripts/create_topic.sh <topic_name>
```

#### List the topic

```
./scripts/list_topic.sh
```

#### Set the right configuration in .env
**You also need set the right env file:**<br>
remove the origin content in .env and copy the key/local-env.txt to the .env.

## Install development environment
---
You can install a local development environment. Please following the following process: 

* Install [Python3.8](https://www.python.org/downloads/)
* Create a venv:

    ```
    python3 -m venv venv
    ```

* Install the packages:

    ```
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    ```
* Start the monitor

    ```
    invoke monitor
    ```

* Start the etl

    ```
    invoke etl
    ```
##### There are other commands include as following:
* lint check

    ``` bash
    make lint
    ```

* run unit test case

    ``` bash
    make test
    ```

* check the unit test coverage

    Open the htmcov/index.html file

## Refer
---
1. [dockerHub Kafka](https://hub.docker.com/r/bitnami/kafka)
2. [Kafka](https://kafka.apache.org/quickstart)
2. [kafka-python](https://pypi.org/project/kafka-python/)
3. [psycopg2](https://pypi.org/project/psycopg2/)
4. [psutil examples](https://programtalk.com/python-examples/psutil.Process/)
5. [pytest-mock](https://pypi.org/project/pytest-mock/)
6. [coverage](https://coverage.readthedocs.io/en/coverage-5.0/)


