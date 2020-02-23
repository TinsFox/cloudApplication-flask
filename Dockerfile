FROM python:3.7-stretch as debian
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app

RUN  apt-get update && pip3 install -r requirements.txt