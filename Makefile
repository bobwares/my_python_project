# Makefile for Python + Poetry + Tox + Pre-commit project

# Core commands
install:
	poetry install --with dev,test,docs

run:
	poetry run python src/my_package/__init__.py

# Tests
test:
	poetry run pytest

tox:
	tox

# Linters and formatters
lint:
	poetry run flake8 src/ tests/

format:
	poetry run black src/ tests/
	poetry run isort src/ tests/
	poetry run autoflake --in-place --remove-all-unused-imports --remove-unused-variables -r src/ tests/

# Pre-commit
hooks-install:
	poetry run pre-commit install

hooks-run:
	poetry run pre-commit run --all-files

# Cleanup
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete
