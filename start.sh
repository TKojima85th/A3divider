#!/bin/bash

# Render startup script for A3→A4 PDF Splitter

echo "Starting A3→A4 PDF Splitter..."

# Set environment variables
export FLASK_ENV=production
export PYTHONPATH="${PYTHONPATH}:."

# Create necessary directories
mkdir -p /tmp/pdf_processing

# Start the application with Gunicorn
exec gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --max-requests 1000 --max-requests-jitter 100 app:app