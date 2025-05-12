.PHONY: install run test lint format coverage docs

install:
	poetry install --with=docs --with=dev --with=test

run:
	uvicorn customer_api.main:app --reload

test:
	pytest

lint:
	black --check src tests
	flake8 src tests

format:
	black src tests

coverage:
	pytest --cov=src/${PACKAGE_NAME}

docs:
	mkdocs serve
