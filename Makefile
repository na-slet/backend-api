include .env
export

ALEMBIC = database

shell:
	poetry shell

prepare:
	poetry install || true

run:
	poetry run uvicorn api.__main__:app --host 0.0.0.0 --port ${FASTAPI_PORT} --log-level critical

clear:
	docker kill na-slet-client-api || true

build:
	docker build -t na-slet-client-api --no-cache .

down:
	docker container stop na-slet-client-api || true

run-docker:
	docker container rm na-slet-client-api || true
	docker run --name  na-slet-client-api -d -p ${FASTAPI_PORT}:${FASTAPI_PORT} na-slet-client-api