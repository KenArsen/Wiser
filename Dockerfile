FROM public.ecr.aws/docker/library/python:3.11
#FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENV_FILE=.env

WORKDIR /app

RUN pip install --upgrade pip \
    && apt-get update

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8080

# Очищаем кэш pip и временные файлы
RUN pip cache purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/*

CMD ["/app/entrypoint.sh"]
