import json
import logging
import shutil
import sys
from argparse import ArgumentParser

from .build_dict import build
from .const import LIBIME_BIN_NAME, LIBIME_REPOLOGY_URL
from .logging import DEFAULT_LOG_LEVEL_STRING, LOG_LEVEL_MAPPING, setup_logger, update_log_level
from .utils import sanitize, is_libime_used, smart_rewrite, try_file


def get_args(args):
    parser = ArgumentParser(
        usage="Fetch titles from online and generate a dictionary.")
    parser.add_argument("-c",
                        "--config",
                        dest="config",
                        default="config.py",
                        help="configuration file location")
    parser.add_argument("-n",
                        "--name",
                        dest="name",
                        default="exports",
                        help="configuration object name")
    parser.add_argument('--log-level',
                        dest="log_level",
                        default=DEFAULT_LOG_LEVEL_STRING,
                        help="log level",
                        choices=LOG_LEVEL_MAPPING.keys())

    return parser.parse_args(args)


def inner_main(args):
    log = logging.getLogger(__name__)
    options = get_args(args)
    update_log_level(options.log_level)
    file = options.config
    objname = options.name
    if file.endswith(".py"):
        config_base = try_file(file)
        if not config_base:
            # I don't think it works... but let's put it here
            config_base = try_file(file + ".py")
    else:
        config_base = try_file(file + ".py")
    if not config_base:
        filename = f"{file}, {file}.py" if file.endswith("py") else file
        log.error("Config file %s not found or not readable", filename)
        sys.exit(1)
    log.debug("Parsing config file: %s", file)
    if objname not in dir(config_base):
        log.error(
            "Exports not found. Please make sure your config in in a object called '%s'.", objname
        )
        sys.exit(1)
    config_object = getattr(config_base, objname)
    log.debug("Config load:")
    displayable_config_object = sanitize(config_object)
    if not isinstance(config_object, object):
        log.error("Invalid config")
        sys.exit(1)
    log.debug(
        json.dumps(displayable_config_object, indent=2, sort_keys=True))
    config_object = smart_rewrite(config_object)
    if is_libime_used(config_object) and shutil.which(LIBIME_BIN_NAME) is None:
        log.warning(
            "You are trying to generate fcitx dictionary, while %s doesn't seem to exist.",
            LIBIME_BIN_NAME
        )
        log.warning(
            "This might cause issues. Please install libime: %s", LIBIME_REPOLOGY_URL
        )
    build(config_object)


def main():
    setup_logger()
    inner_main(sys.argv[1:])
