FROM ubuntu:bionic

RUN apt-get update && apt-get install --no-install-recommends --yes python3.8-dev python3-pip python3-setuptools python3-wheel binutils

WORKDIR /app

COPY requirements.txt .

RUN python3.8 -m pip install -r requirements.txt

COPY main.py .

ENV UID=0
ENV GID=0
