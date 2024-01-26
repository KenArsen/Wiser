FROM public.ecr.aws/docker/library/python:3.10
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV_FILE .env_local

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

#ADD . /wiser_load_board_back/
#RUN apt-get update && apt-get install -y redis-server

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

COPY . /app/

EXPOSE 8080

# Use the entrypoint script to start both Celery and your Django app
CMD ["/app/entrypoint.sh"]