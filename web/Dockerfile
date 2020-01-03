FROM python:3.8

LABEL maintainer="minnigaliev-r@yandex.ru"

WORKDIR /app

RUN sed -i '/ *#/d; /^$/d; s/[a-z]*.debian.org/mirror.yandex.ru/g' /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        nano cron supervisor \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt && rm -f requirements.txt

COPY config/cron/web /etc/cron.d/web

ENTRYPOINT /usr/bin/supervisord
