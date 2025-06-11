import logging
import os

from mw2fcitx.const import LOG_LEVEL_ENV_VARIABLE


LOG_LEVEL_MAPPING = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

DEFAULT_LOG_LEVEL_STRING = "DEBUG"
DEFAULT_LOG_LEVEL = LOG_LEVEL_MAPPING[DEFAULT_LOG_LEVEL_STRING]

log = logging.getLogger(__name__)


def setup_logger():
    logging.basicConfig(
        level=DEFAULT_LOG_LEVEL,
        format='%(asctime)s %(name)s %(levelname)s - %(message)s',
    )


def update_log_level(args_log_level_str: str):
    override_log_level = LOG_LEVEL_MAPPING.get(args_log_level_str)
    if override_log_level is None:
        log.warning(f"Invalid --log-level: {args_log_level_str}, ignoring")
    env_log_level_str = os.environ.get(LOG_LEVEL_ENV_VARIABLE)
    if env_log_level_str is not None:
        env_override_log_level = LOG_LEVEL_MAPPING.get(env_log_level_str)
        if env_override_log_level is None:
            log.warning(
                f"Invalid environment variable {LOG_LEVEL_ENV_VARIABLE}: {env_log_level_str}, ignoring")
        else:
            override_log_level = env_override_log_level
    if override_log_level is not None:
        logging.getLogger().setLevel(override_log_level)
