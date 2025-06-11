import logging
import os

import pytest
from mw2fcitx.logging import setup_logger, update_log_level, DEFAULT_LOG_LEVEL


@pytest.fixture(autouse=True)
def reset_logging():
    yield
    if os.environ.get("LOG_LEVEL") is not None:
        del os.environ["LOG_LEVEL"]
    logging.getLogger().setLevel(logging.NOTSET)


def test_args_good():
    update_log_level("CRITICAL")
    assert (
        logging.getLogger().level == logging.CRITICAL
    )


def test_args_bad():
    update_log_level("NOTGOOD")
    assert (
        logging.getLogger().level == logging.NOTSET
    )


def test_envvar_override():
    os.environ["LOG_LEVEL"] = "CRITICAL"
    update_log_level("WARNING")
    assert (
        logging.getLogger().level == logging.CRITICAL
    )


def test_envvar_bad():
    os.environ["LOG_LEVEL"] = "NOTGOOD"
    update_log_level("WARNING")
    assert (
        logging.getLogger().level == logging.WARNING
    )
