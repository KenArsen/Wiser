FROM public.ecr.aws/docker/library/python:3.11
ENV PYTHONUNBUFFERED 1
ENV ENV_FILE .env

WORKDIR /wiser_load_board_back
RUN pip install --upgrade pip

COPY requirements.txt /wiser_load_board_back/
RUN pip install -r /wiser_load_board_back/requirements.txt

ADD . /wiser_load_board_back/

EXPOSE 8000
RUN mkdir "static"

CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput"

CMD ["gunicorn","--bind", ":8000", "wiser_load_board.wsgi:application"]