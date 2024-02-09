#!/bin/sh

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Start Celery worker
celery -A wiser_load_board worker --loglevel=info &

# Start Celery beat
celery -A wiser_load_board beat --loglevel=info &

# Start Gunicorn server
exec gunicorn --bind :8080 wiser_load_board.wsgi:application