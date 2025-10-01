#!/bin/bash
set -e

echo "🔄 Waiting for PostgreSQL to be ready..."

# Wait for PostgreSQL to be ready
while ! nc -z postgres 5432; do
  echo "⏳ Waiting for PostgreSQL..."
  sleep 1
done

echo "✅ PostgreSQL is ready!"

# Run migrations
echo "🚀 Running database migrations..."
cd /app/src/infrastructure/persistence/migrations

# Set PYTHONPATH so alembic can import modules
export PYTHONPATH=/app/src

# Run alembic upgrade
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully!"
else
    echo "❌ Migration failed!"
    exit 1
fi

# Go back to src directory
cd /app/src

echo "🚀 Starting FastAPI application..."

# Execute the main command (from docker-compose or CMD)
exec "$@"