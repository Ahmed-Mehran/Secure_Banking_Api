#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

python /app/docker/local/django/wait_for_db.py

echo "PostgreSQL is available"

exec "$@"






















