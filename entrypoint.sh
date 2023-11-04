#!/bin/sh

# Set execute permissions for entrypoint.sh (optional)
chmod +x /wiser_load_board_back/entrypoint.sh

# Start Celery worker in the background
python -m celery -A wiser_load_board worker -l info &

# Start Celery beat in the background
python -m celery -A wiser_load_board beat --loglevel=info &

# Start your Django application
exec /bin/sh -c "python manage.py migrate && gunicorn --bind :8080 wiser_load_board.wsgi:application"
