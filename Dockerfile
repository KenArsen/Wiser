FROM public.ecr.aws/docker/library/python:3.11
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV_FILE .env

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .

COPY . .

EXPOSE 8080

# Set permissions for entrypoint script
RUN chmod +x entrypoint.sh

# Use the entrypoint script to start both Celery and your Django app
CMD ["/app/entrypoint.sh"]