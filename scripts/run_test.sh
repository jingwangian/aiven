#!/bin/bash

echo "Start unittesting ..."
docker-compose run monitor pytest --cov-config=.coveragerc --cov-report=html --cov=app
echo "Done"
