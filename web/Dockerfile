FROM python:3.8

LABEL maintainer="minnigaliev-r@yandex.ru"

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt && rm -f requirements.txt
