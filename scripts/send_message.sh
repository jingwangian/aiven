#!/bin/bash

topic=$1
CMD=/opt/bitnami/kafka/bin/kafka-console-producer.sh

if [ ${topic}x = x ]
then
  echo "Please input topic as parameter"
  exit 0
fi

docker-compose exec kafka ${CMD} --broker-list localhost:9092 --topic ${topic}
