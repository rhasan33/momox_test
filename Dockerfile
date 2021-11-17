FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir data

RUN apt-get update && apt-get install build-essential curl -y && \
    pip3 install -U pip

ADD requirements.txt /app/

RUN pip install -r requirements.txt

COPY src/ /app/

RUN echo ls