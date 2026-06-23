#!/bin/bash
# Render deployment startup script
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Importing content..."
python manage.py import_content --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
gunicorn laver_website.wsgi:application
