#!/bin/sh

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

# Clear Celery Beat cache
rm -rf celerybeat-schedule.*

# Start Celery worker
celery -A wiser_load_board worker -l info --without-gossip --without-mingle --without-heartbeat &

# Start Celery beat
celery -A wiser_load_board beat -l info &

# Start Gunicorn server
#exec gunicorn --bind :8080 wiser_load_board.wsgi:application
exec daphne -b 0.0.0.0 -p 8080 wiser_load_board.asgi:application