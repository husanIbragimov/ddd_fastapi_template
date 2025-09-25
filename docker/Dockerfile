FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ../requirements.txt .
COPY ../pyproject.toml .
RUN pip install --upgrade pip && pip install -r requirements.txt

WORKDIR /app/src