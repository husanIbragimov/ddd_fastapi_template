FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-openbsd && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ../requirements.txt .
COPY ../pyproject.toml .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

WORKDIR /app/src

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command (will be executed by entrypoint)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
