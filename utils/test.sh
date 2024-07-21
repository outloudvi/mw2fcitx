#!/bin/bash
set -e

poetry install
poetry shell
coverage erase
coverage run -m pytest tests/lib
coverage run -a -m mw2fcitx.main -c tests/cli/conf_one.py
coverage html
