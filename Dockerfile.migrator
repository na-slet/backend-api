FROM python:3.10-alpine
WORKDIR /code
RUN apk add --no-cache make
RUN apk add --no-cache poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install || true
COPY ./database ./database
COPY ./.env ./.env
COPY ./Makefile ./Makefile
CMD make migrate