#!/bin/sh

python manage.py migrate &

python manage.py collectstatic --no-input &

python manage.py shell -c "from apps.user.models import User; \
User.objects.create_superuser('superadmin@gmail.com', '123') if not User.objects.filter(email='superadmin@gmail.com').exists() else None"

# Start Celery worker in the background
python -m celery -A wiser_load_board worker -l info &

# Start Celery beat in the background
python -m celery -A wiser_load_board beat --loglevel=info &

# Start your Django application
exec /bin/sh -c "gunicorn --bind :8080 wiser_load_board.wsgi:application"

chmod +x entrypoint.sh