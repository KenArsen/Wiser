# Start Celery worker in the background
python -m celery -A wiser_load_board.celery worker -l info &
python -m celery -A wiser_load_board beat --loglevel=info &


# Start your Django application
exec /bin/sh -c "python manage.py migrate && gunicorn --bind :8080 wiser_load_board.wsgi:application"

chmod +x entrypoint.sh