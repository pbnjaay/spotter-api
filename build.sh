#!/bin/bash

# Exit on error
set -e

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running migrations..."
python manage.py migrate

echo "Build completed successfully!"
