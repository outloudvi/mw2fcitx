import json
import logging
import shutil
import sys
from argparse import ArgumentParser


from .build_dict import build
from .const import LIBIME_BIN_NAME, LIBIME_REPOLOGY_URL
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

    return parser.parse_args(args)


def inner_main(args):
    log = logging.getLogger(__name__)
    options = get_args(args)
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
        log.error(f"Config file {filename} not found or not readable")
        sys.exit(1)
    log.debug(f"Parsing config file: {file}")
    if objname not in dir(config_base):
        log.error(
            f"Exports not found. Please make sure your config in in a object called '{objname}'."
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
            f"You are trying to generate fcitx dictionary, "
            f"while {LIBIME_BIN_NAME} doesn't seem to exist."
        )
        log.warning(
            f"This might cause issues. "
            f"Please install libime: {LIBIME_REPOLOGY_URL}"
        )
    build(config_object)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s - %(message)s',
    )
    inner_main(sys.argv[1:])
