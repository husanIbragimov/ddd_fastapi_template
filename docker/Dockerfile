FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TEMPLATE_DEV=prod

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../requirements.txt /app/
RUN pip install -r requirements.txt

COPY ../src /app/src

ENV PYTHONPATH=/app/src
