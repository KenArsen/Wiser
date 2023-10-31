FROM public.ecr.aws/docker/library/python:3.11
ENV PYTHONUNBUFFERED 1
ENV ENV_FILE .env

WORKDIR /wiser_load_board_back
RUN pip install --upgrade pip

COPY requirements.txt /wiser_load_board_back/
RUN pip install -r /wiser_load_board_back/requirements.txt

ADD . /wiser_load_board_back/

EXPOSE 8080
RUN mkdir "static"
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@gmail.com', 'adminpassword')" | python manage.py shell
CMD ["/bin/sh", "-c", "python manage.py migrate && gunicorn --bind :8000 wiser_load_board.wsgi:application"]