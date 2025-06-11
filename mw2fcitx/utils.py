import sys
import re
from copy import deepcopy
from importlib import import_module
import os
import logging
from typing import List
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter


from .version import PKG_VERSION

log = logging.getLogger(__name__)


def normalize(word):
    return word.strip()


def sanitize(obj):
    res = deepcopy(obj)
    typ = type(res)
    if typ == type(sanitize):  # function
        func_name = res.__name__ or "lambda"
        return f"[func {func_name}]"
    if typ == type({}):  # object
        for i in res.keys():
            res[i] = sanitize(res[i])
    elif typ == type([]):  # list
        fin = []
        for i in res:
            fin.append(sanitize(i))
        res = fin
    elif typ == type(1) or typ == type("1"):  # number
        return str(res)
    else:  # whatever
        return "[" + str(type(res)) + "]"
    return res


def smart_rewrite(config_object):

    # If `generator` is not a list, make it a list
    generators = config_object["generator"]
    if not isinstance(generators, list):
        config_object["generator"] = [generators]

    # If `title_file_path` is not a list, make it a list
    title_file_path = config_object["source"].get("file_path")
    if isinstance(title_file_path, str):
        config_object["source"]['file_path'] = [title_file_path]

    return config_object


def is_libime_used(config):
    generators = config.get('generator') or []
    for i in generators:
        if i.get("use") == "pinyin":
            return True
    return False


def dedup(arr: List[str]):
    return list(set(arr))


def create_requests_session():
    s = Session()
    retries = Retry(
        total=3,
        backoff_factor=1,
    )
    s.headers.update({
        "User-Agent": f"MW2Fcitx/{PKG_VERSION}; github.com/outloudvi/fcitx5-pinyin-moegirl",
    })
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s


def try_file(file):
    log.debug(f"Finding config file: {file}")
    if not os.access(file, os.R_OK):
        log.error("File ({}) not readable.")
        return False
    file_realpath = os.path.realpath(file)
    log.debug(f"Config file path: {file_realpath}")
    file_path = os.path.dirname(file_realpath)
    file_name = os.path.basename(file_realpath)
    module_name = re.sub(r"\.py$", "", file_name)
    config_file = False
    try:
        sys.path.insert(1, file_path)
        config_file = import_module(module_name)
    except Exception as e:
        log.error(f"Error reading config: {str(e)}")
        return False
    finally:
        sys.path.remove(file_path)
    return config_file
