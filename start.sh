#!/bin/bash
# Startup script for Railway deployment

# Use PORT from environment or default to 5000
PORT=${PORT:-5000}

echo "Starting Gunicorn on port $PORT..."

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 60 app:app
