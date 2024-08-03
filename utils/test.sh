#!/bin/bash
set -e

poetry install
poetry run coverage erase
poetry run coverage run -m pytest tests/
poetry run coverage run -a -m mw2fcitx.main -c tests/cli/conf_one.py
poetry run coverage html
