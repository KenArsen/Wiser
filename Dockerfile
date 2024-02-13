FROM public.ecr.aws/docker/library/python:3.11
#FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV_FILE=.env_local

WORKDIR /app

RUN pip install --upgrade pip \
    && apt-get update

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir static \
    && chmod +x entrypoint.sh

EXPOSE 8080

CMD ["/app/entrypoint.sh"]
