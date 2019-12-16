FROM python:3.8.0-slim-buster

LABEL maintainer "Ian Wang <jingwangian@gmail.com>"

USER root
WORKDIR /tmp
COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && apt-get install -y build-essential

RUN pip3 --no-cache install -r /tmp/requirements.txt

COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip3 --no-cache install -r /tmp/requirements-dev.txt

WORKDIR /opt/aiven
