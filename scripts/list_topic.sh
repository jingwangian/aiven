#!/bin/bash

CMD=/opt/bitnami/kafka/bin/kafka-topics.sh

echo "Listing topic ..."

# ${CMD} --list --bootstrap-server localhost:9092

docker-compose exec kafka ${CMD} --list --bootstrap-server localhost:9092
