#!/bin/sh

echo "================================="
echo "Docker Entrypoint Script Started"
echo "================================="

echo "Running initialization tasks..."

mkdir -p /app/logs

echo "Initialization completed!"

echo "Received arguments: $@"

exec "$@"
