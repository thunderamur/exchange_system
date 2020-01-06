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
RUN chmod 0644 /etc/cron.d/web

COPY config/sv/supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY exchange_system.env /etc/environment

ENTRYPOINT /usr/bin/supervisord
