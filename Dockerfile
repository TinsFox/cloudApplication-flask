FROM python:3.7-stretch as debian
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app

RUN  apt-get update && apt install vim && pip3 install -r requirements.txt
CMD ["gunicorn -b 0.0.0.0:5000 run:app"]