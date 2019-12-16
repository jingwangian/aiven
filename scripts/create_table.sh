#!/bin/bash

echo "Creating tables ..."
docker-compose run monitor invoke initdb
echo "Done"
