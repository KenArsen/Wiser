FROM public.ecr.aws/docker/library/python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV_FILE .env

WORKDIR /app
RUN pip install --upgrade pip

COPY requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/
RUN apt-get update && apt-get install -y redis-server
RUN mkdir "static"

COPY entrypoint.sh .

COPY . .

EXPOSE 8080

# Set permissions for entrypoint script
RUN chmod +x entrypoint.sh

# Clear Celery cache
RUN rm -rf /app/celerybeat-schedule*

# Use the entrypoint script to start both Celery and your Django app
CMD ["/app/entrypoint.sh"]