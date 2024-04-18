#!/bin/sh

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input

python manage.py shell -c "from apps.user.models import User; \
 User.objects.create_superuser('superadmin@gmail.com', '123') if not User.objects.filter(email='superadmin@gmail.com').exists() else None"

# Clear Celery Beat cache
rm -rf celerybeat-schedule.*

# Start Celery worker
celery -A wiser_load_board worker -l info --without-gossip --without-mingle --without-heartbeat &

# Start Celery beat
celery -A wiser_load_board beat -l info &

# Start Gunicorn server
exec gunicorn --bind :8080 wiser_load_board.wsgi:application