.PHONY: test

help:
	@echo "test             run test"

build:
	poetry build

test:
	poetry run pytest tests/

lint:
	poetry run autopep8 --in-place mw2fcitx/**/*.py