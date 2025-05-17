.PHONY: test

help:
	@echo "test             run test"

build:
	poetry build

test:
	poetry run pytest tests/ --ignore=tests/opencc

test_opencc:
	poetry run pytest tests/opencc

lint:
	poetry run pylint **/*.py

format:
	poetry run autopep8 --in-place mw2fcitx/**/*.py

test_version:
	@bash scripts/test_version.sh