FROM python:3.10.8-slim-buster
WORKDIR /bank

COPY requirements.txt ./tmp/

COPY ./bank .


RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install --no-cache-dir --upgrade -r ./tmp/requirements.txt


ENV DATABASE_HOST='db'

EXPOSE 8000