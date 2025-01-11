import sys
import json
from os import access, R_OK
import time
from urllib.parse import quote_plus
import urllib3

from .version import PKG_VERSION
from .logger import console

http = urllib3.PoolManager()

HEADERS = {
    "User-Agent": f"MW2Fcitx/{PKG_VERSION}; github.com/outloudvi/fcitx5-pinyin-moegirl",
    "Accept-Encoding": "gzip, deflate"
}


def save_to_partial(partial_path, titles, apcontinue):
    ret = {"apcontinue": apcontinue, "titles": titles}
    try:
        with open(partial_path, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(ret, ensure_ascii=False))
        console.debug(f"Partial session saved to {partial_path}")
    except Exception as e:
        console.error(str(e))


def resume_from_partial(partial_path):
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


def fetch_all_titles(api_url, **kwargs):
    limit = kwargs.get("api_title_limit") or kwargs.get("title_limit") or -1
    console.debug(f"Fetching titles from {api_url}" +
                  (f" with a limit of {limit}" if limit != -1 else ""))
    titles = []
    partial_path = kwargs.get("partial")
    time_wait = float(kwargs.get("request_delay", "2"))
    _aplimit = kwargs.get("aplimit", "max")
    aplimit = int(_aplimit) if _aplimit != "max" else "max"
    fetch_url = api_url + \
        f"?action=query&list=allpages&aplimit={aplimit}&format=json"
    if partial_path is not None:
        console.info(f"Partial session will be saved/read: {partial_path}")
        [titles, apcontinue] = resume_from_partial(partial_path)
        if apcontinue is not None:
            fetch_url += f"&apcontinue={quote_plus(apcontinue)}"
            console.info(
                f"{len(titles)} titles found. Continuing from {apcontinue}")
    resp = http.request("GET", fetch_url, headers=HEADERS, retries=3)
    data = resp.json()
    break_now = False
    while True:
        for i in map(lambda x: x["title"], data["query"]["allpages"]):
            titles.append(i)
            if limit != -1 and len(titles) >= limit:
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
                data = http.request("GET", api_url +
                                    f"?action=query&list=allpages&format=json"
                                    f"&aplimit={aplimit}"
                                    f"&apcontinue={quote_plus(apcontinue)}",
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
    console.info("Finished.")
    return titles
