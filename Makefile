include .env
export

ALEMBIC = migrator

migrate:
	cd ${ALEMBIC} && poetry run alembic upgrade head

revision:
	cd ${ALEMBIC} && poetry run alembic revision --autogenerate

upgrade:
	cd ${ALEMBIC} && poetry run alembic upgrade +1

downgrade:
	cd ${ALEMBIC} && poetry run alembic downgrade -1

shell:
	poetry shell

prepare:
	poetry install || true

run:
	poetry run uvicorn api.__main__:app --host 0.0.0.0 --port ${FASTAPI_PORT} --log-level critical

down:
	docker-compose down || true

rebuild:
	docker build --no-cache .

build:
	docker build .

logs:
	docker-compose logs

postgresql:
	docker-compose up -d postgresql

migrator:
	docker-compose up migrator

api:
	docker-compsoe up -d api

up:
	docker-compose up -d

open_postgresql:
	PGPASSWORD=${DB_PASSWORD} docker exec -it na-slet-postgresql psql -h localhost -U ${DB_USERNAME} -d ${DB_NAME}
