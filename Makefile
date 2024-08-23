.PHONY: test

help:
	@echo "test             run test"

build:
	poetry build

test:
	poetry run pytest tests/