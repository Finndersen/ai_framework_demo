.PHONY: install test lint clean

install:
	pip install -e ".[dev]"

test:
	pytest

format:
	ruff format .
	ruff check . --fix

lint:
	ruff format . --check
	ruff check .
	mypy src
