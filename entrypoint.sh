#!/bin/sh

python manage.py migrate

python manage.py collectstatic --no-input

# Start Celery worker in the background
python -m celery -A wiser_load_board worker -l info

# Start Celery beat in the background
python -m celery -A wiser_load_board beat --loglevel=info

# Start your Django application
exec /bin/sh -c "gunicorn --bind :8000 wiser_load_board.wsgi:application"

chmod +x entrypoint.sh