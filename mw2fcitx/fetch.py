import logging
import sys
import json
from os import access, R_OK
import time
from typing import Any, List, Union

from requests import Session

from .const import ADVANCED_MODE_TRIGGER_PARAMETER_NAMES, \
    PARTIAL_CONTINUE_DICT, \
    PARTIAL_DEPRECATED_APCONTINUE, \
    PARTIAL_TITLES
from .utils import create_requests_session

log = logging.getLogger(__name__)


def save_to_partial(partial_path: str, titles: List[str], continue_dict: dict):
    ret = {PARTIAL_CONTINUE_DICT: continue_dict, PARTIAL_TITLES: titles}
    try:
        with open(partial_path, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(ret, ensure_ascii=False))
        log.debug("Partial session saved to %s", partial_path)
    except Exception as e:
        log.error(str(e))


def resume_from_partial(partial_path: str) -> tuple[List[str], dict]:
    if not access(partial_path, R_OK):
        log.warning("Cannot read partial session: %s", partial_path)
        return ([], {})
    try:
        with open(partial_path, "r", encoding="utf-8") as fp:
            partial_data = json.load(fp)
            titles = partial_data.get(PARTIAL_TITLES, [])
            deprecated_apcontinue = partial_data.get(
                PARTIAL_DEPRECATED_APCONTINUE, None)
            continue_dict = partial_data.get(PARTIAL_CONTINUE_DICT, None)
            if continue_dict is None and deprecated_apcontinue is not None:
                continue_dict = {
                    "apcontinue": deprecated_apcontinue
                }
            return (titles, continue_dict)
    except Exception as e:
        log.error(str(e))
        log.error("Failed to parse partial session")
        return ([], {})


def warn_advanced_mode(custom_api_params: dict, triggerer_param_names: List[str]) -> bool:
    is_advanced_mode = False
    for param_name in triggerer_param_names:
        if param_name in custom_api_params:
            log.warning(
                "I'm seeing `%s` in `api_params`. "
                "Advanced Mode is enabled. "
                "No parameter except for `format` will be injected automatically.", param_name
            )
            is_advanced_mode = True

    return is_advanced_mode


def populate_api_params(custom_api_params: dict, deprecated_aplimit: Union[None, int]) -> dict:
    api_params = {
        "format": "json"
    }

    if not warn_advanced_mode(custom_api_params, ADVANCED_MODE_TRIGGER_PARAMETER_NAMES):
        # Deprecated `aplimit`
        if deprecated_aplimit is not None:
            log.warning(
                "Warn: `source.kwargs.aplimit` is deprecated - "
                "please use `source.kwargs.api_param.aplimit` instead.")
        aplimit = int(deprecated_aplimit) \
            if deprecated_aplimit != "max" and deprecated_aplimit is not None \
            else "max"
        if "aplimit" not in custom_api_params:
            custom_api_params["aplimit"] = aplimit

        api_params.update({
            # default params
            "aplimit": "max",
            "action": "query",
            "list": "allpages",
        })

    api_params.update(custom_api_params)
    return api_params


def fetch_all_titles(api_url: str, **kwargs) -> List[str]:
    title_limit = kwargs.get(
        "api_title_limit") or kwargs.get("title_limit") or -1
    log_msg = f"Fetching titles from {api_url}" + \
        (f" with a limit of {title_limit}" if title_limit != -1 else "")
    log.debug(log_msg)
    titles = []
    partial_path = kwargs.get("partial")
    time_wait = float(kwargs.get("request_delay", "2"))
    custom_api_params = kwargs.get("api_params", {})
    if not isinstance(custom_api_params, dict):
        log.error(
            "Type of `api_params` is not dict or None, but %s", type(custom_api_params))
        sys.exit(1)

    api_params = populate_api_params(custom_api_params, kwargs.get("aplimit"))
    if partial_path is not None:
        log.info("Partial session will be saved/read: %s", partial_path)
        [titles, continue_dict] = resume_from_partial(partial_path)
        if continue_dict is not None:
            api_params.update(continue_dict)
            log.info(
                "%d titles found. Continuing from %s", len(titles), continue_dict)
    s = create_requests_session(kwargs.get("user_agent"))
    resp = s.get(api_url, params=api_params)
    initial_data = resp.json()
    titles = fetch_all_titles_inner(
        titles,
        initial_data,
        title_limit,
        api_url,
        api_params,
        partial_path,
        time_wait,
        s
    )
    log.info("Finished.")
    return titles


def fetch_all_titles_inner(
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    titles: List[str],
    initial_data: Any,
    title_limit: int,
    api_url: str,
    initial_api_params: dict,
    partial_path: Union[str, None],
    time_wait: float,
    s: Session
) -> List[str]:
    data = initial_data

    while True:
        if "error" in data:
            error_code = data["error"].get("code", "?")
            error_msg = data["error"].get("info", str(data["error"]))
            log.error(
                "MediaWiki API error: [code: %s] %s", error_code, error_msg
            )
        if not "query" in data:
            log.error(
                "No `query` found in response. "
                "Please check the response body for any potential issues:"
            )
            log.error(data)
            sys.exit(1)

        for (_, item_value) in data["query"].items():
            titles += list(map(lambda x: x["title"], item_value))
        if title_limit != -1 and len(titles) >= title_limit:
            titles = titles[:title_limit]
            break
        log.debug("Got %s pages", len(titles))
        if "continue" in data:
            time.sleep(time_wait)
            continue_dict = {}
            try:
                continue_dict = data["continue"]
                log.debug("Continuing from %s", continue_dict)
                api_params = initial_api_params.copy()
                api_params.update(continue_dict)
                data = s.get(api_url, params=api_params).json()
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    log.error("Keyboard interrupt received. Stopping.")
                else:
                    log.error(str(e))
                if partial_path:
                    save_to_partial(partial_path, titles, continue_dict)
                sys.exit(1)
        else:
            break

    return titles
