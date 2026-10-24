#!/bin/sh

echo "Docker Entrypoint Started!"

echo "Environment: ${APP_ENV:-development}"

if [ "$APP_ENV" = "production" ]; then
    echo "Running production initialization..."
else
    echo "Running development initialization..."
fi

exec "$@"
