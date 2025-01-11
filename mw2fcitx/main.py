import json
import os
import re
import shutil
import sys
from argparse import ArgumentParser
from importlib import import_module

from .build_dict import build
from .const import LIBIME_BIN_NAME, LIBIME_REPOLOGY_URL
from .logger import console
from .utils import sanitize, is_libime_used, smart_rewrite


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


def try_file(file):
    console.debug(f"Finding config file: {file}")
    if not os.access(file, os.R_OK):
        console.error("File ({}) not readable.")
        return False
    file_realpath = os.path.realpath(file)
    console.debug(f"Config file path: {file_realpath}")
    file_path = os.path.dirname(file_realpath)
    file_name = os.path.basename(file_realpath)
    module_name = re.sub(r"\.py$", "", file_name)
    config_file = False
    try:
        sys.path.insert(1, file_path)
        config_file = import_module(module_name)
    except Exception as e:
        console.error(f"Error reading config: {str(e)}")
        return False
    finally:
        sys.path.remove(file_path)
    return config_file


def inner_main(args):
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
        console.error(f"Config file {filename} not found or not readable")
        sys.exit(1)
    console.debug(f"Parsing config file: {file}")
    if objname not in dir(config_base):
        console.error(
            f"Exports not found. Please make sure your config in in a object called '{objname}'."
        )
        sys.exit(1)
    config_object = getattr(config_base, objname)
    console.debug("Config load:")
    displayable_config_object = sanitize(config_object)
    if not isinstance(config_object, object):
        console.error("Invalid config")
        sys.exit(1)
    console.debug(
        json.dumps(displayable_config_object, indent=2, sort_keys=True))
    config_object = smart_rewrite(config_object)
    if is_libime_used(config_object) and shutil.which(LIBIME_BIN_NAME) is None:
        console.warning(
            f"You are trying to generate fcitx dictionary, "
            f"while {LIBIME_BIN_NAME} doesn't seem to exist."
        )
        console.warning(
            f"This might cause issues. "
            f"Please install libime: {LIBIME_REPOLOGY_URL}"
        )
    build(config_object)


def main():
    inner_main(sys.argv[1:])
