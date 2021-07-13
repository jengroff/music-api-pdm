#!/bin/sh

echo "Waiting for postgres..."

# netcat command to listen on port 5432 until there is a response
# the -z option stands for zero-I/O mode, which is used for scanning

while ! nc -z web-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

exec "$@"