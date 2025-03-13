#!/bin/bash
set -e

echo "Starting the backend..."

# Add the current directory to PYTHONPATH
export PYTHONPATH=/app:$PYTHONPATH

# Wait for the database to be ready
echo "Waiting for the database to be ready..."
python -m scripts.wait_for_db

# Create the database if it doesn't exist
echo "Creating the database if it doesn't exist..."
python -m scripts.create_db

# Start the FastAPI application
echo "Starting the FastAPI application..."
python -muvicorn main:app --host 0.0.0.0 --port 8000 --reload
