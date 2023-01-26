# build stage
FROM python:3.10-slim-bullseye as build

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements requirements

RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements/development.txt


# final stage
FROM python:3.10-slim-bullseye

WORKDIR /app

COPY --from=build /app/wheels wheels
COPY --from=build /app/requirements/development.txt .

RUN pip install --no-cache wheels/*
