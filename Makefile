.PHONY: test

help:
	@echo "test             run test"

build:
	poetry build

test:
	poetry run pytest tests/
	poetry run mw2fcitx -c tests/cli/conf_one.py