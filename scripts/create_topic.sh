#!/bin/bash

topic=$1
CMD=/opt/bitnami/kafka/bin/kafka-topics.sh


if [ ${topic}x = x ]
then
  echo "Please input topic as parameter"
  exit 0
fi

echo "You are creating topic: ${topic}"

docker-compose exec kafka ${CMD} --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic ${topic}
