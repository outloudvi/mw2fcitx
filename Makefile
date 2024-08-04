.PHONY: test

help:
	@echo "test             run test"

test:
	poetry run pytest tests/
	poetry run mw2fcitx -c tests/cli/conf_one.py