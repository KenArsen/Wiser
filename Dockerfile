FROM public.ecr.aws/docker/library/python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV_FILE .env

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

COPY . /app/

EXPOSE 8080

# Use the entrypoint script to start both Celery and your Django app
CMD ["/app/entrypoint.sh"]



