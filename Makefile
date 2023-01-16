include .env
export

ALEMBIC = database

shell:
	poetry shell

prepare:
	poetry install || true

run:
	uvicorn api.__main__:app --host 0.0.0.0 --port ${FASTAPI_PORT} --log-level critical