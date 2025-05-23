from copy import deepcopy
from typing import List
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter


from .version import PKG_VERSION


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
