# Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY ./src /app/src
COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src
