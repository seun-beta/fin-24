FROM python:3.11.0rc2-alpine3.16

WORKDIR /app

RUN apk add --no-cache jpeg-dev zlib-dev

RUN apk add --no-cache --virtual .build-deps build-base linux-headers postgresql-dev  \
    && pip install Pillow && pip install psycopg2

COPY requirements/* ./app/requirements/

RUN pip install -r ./app/requirements/production.txt

COPY . .

ENV ENVIRONMENT=config.settings.development

CMD ["python manage.py runserver"]
