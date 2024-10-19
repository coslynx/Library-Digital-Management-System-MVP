#!/bin/bash

# Exit on error
set -e

# Load environment variables
echo "Loading environment variables..."
source .env

# Start the backend server
echo "Starting backend server..."
uvicorn api.main:app --host $HOST --port $PORT --reload

# Start the database
echo "Starting database..."
docker-compose up -d database

# Check if services are running
echo "Checking if services are running..."
if [[ $(pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER) -eq 0 ]]; then
  echo "Database is not running. Please check database configuration."
  exit 1
fi

echo "All services are running successfully!"