import sys
import json
from os import access, R_OK
import time
from typing import Any, List, Union
from urllib.parse import quote_plus, urlencode
import urllib3

from .version import PKG_VERSION
from .logger import console

http = urllib3.PoolManager()

HEADERS = {
    "User-Agent": f"MW2Fcitx/{PKG_VERSION}; github.com/outloudvi/fcitx5-pinyin-moegirl",
    "Accept-Encoding": "gzip, deflate"
}


def save_to_partial(partial_path: str, titles: List[str], apcontinue: str):
    ret = {"apcontinue": apcontinue, "titles": titles}
    try:
        with open(partial_path, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(ret, ensure_ascii=False))
        console.debug(f"Partial session saved to {partial_path}")
    except Exception as e:
        console.error(str(e))


def resume_from_partial(partial_path: str):
    if not access(partial_path, R_OK):
        console.warning(f"Cannot read partial session: {partial_path}")
        return [[], None]
    try:
        with open(partial_path, "r", encoding="utf-8") as fp:
            partial_data = json.load(fp)
            titles = partial_data.get("titles", [])
            apcontinue = partial_data.get("apcontinue", None)
            return [titles, apcontinue]
    except Exception as e:
        console.error(str(e))
        console.error("Failed to parse partial session")
        return [[], None]


def fetch_all_titles(api_url: str, **kwargs) -> List[str]:
    title_limit = kwargs.get(
        "api_title_limit") or kwargs.get("title_limit") or -1
    console.debug(f"Fetching titles from {api_url}" +
                  (f" with a limit of {title_limit}" if title_limit != -1 else ""))
    titles = []
    partial_path = kwargs.get("partial")
    time_wait = float(kwargs.get("request_delay", "2"))
    if kwargs.get("aplimit") is not None:
        console.warning(
            "Warn: `source.kwargs.aplimit` is deprecated - "
            "please use `source.kwargs.api_param.aplimit` instead.")
    _aplimit = kwargs.get("aplimit", "max")
    aplimit = int(_aplimit) if _aplimit != "max" else "max"
    api_params = kwargs.get("api_params", {})
    if "aplimit" not in api_params:
        api_params["aplimit"] = aplimit
    api_params["action"] = "query"
    api_params["list"] = "allpages"
    api_params["format"] = "json"
    base_fetch_url = f"{api_url}?{urlencode(api_params)}"
    first_fetch_url = base_fetch_url
    if partial_path is not None:
        console.info(f"Partial session will be saved/read: {partial_path}")
        [titles, apcontinue] = resume_from_partial(partial_path)
        if apcontinue is not None:
            first_fetch_url += f"&apcontinue={quote_plus(apcontinue)}"
            console.info(
                f"{len(titles)} titles found. Continuing from {apcontinue}")
    resp = http.request("GET", first_fetch_url, headers=HEADERS, retries=3)
    initial_data = resp.json()
    titles = fetch_all_titles_inner(
        titles,
        initial_data,
        title_limit,
        base_fetch_url,
        partial_path,
        time_wait
    )
    console.info("Finished.")
    return titles


def fetch_all_titles_inner(
    # pylint: disable=too-many-arguments,too-many-positional-arguments
    titles: List[str],
    initial_data: Any,
    title_limit: int,
    base_fetch_url: str,
    partial_path: Union[str, None],
    time_wait: float
) -> List[str]:
    data = initial_data
    break_now = False

    while True:
        for i in map(lambda x: x["title"], data["query"]["allpages"]):
            titles.append(i)
            if title_limit != -1 and len(titles) >= title_limit:
                break_now = True
                break
        console.debug(f"Got {len(titles)} pages")
        if break_now:
            break
        if "continue" in data:
            time.sleep(time_wait)
            try:
                apcontinue = data["continue"]["apcontinue"]
                console.debug(f"Continuing from {apcontinue}")
                data = http.request("GET", base_fetch_url + f"&apcontinue={quote_plus(apcontinue)}",
                                    headers=HEADERS,
                                    retries=3).json()
            except Exception as e:
                if isinstance(e, KeyboardInterrupt):
                    console.error("Keyboard interrupt received. Stopping.")
                else:
                    console.error(str(e))
                if partial_path:
                    save_to_partial(partial_path, titles, apcontinue)
                sys.exit(1)
        else:
            break

    return titles
