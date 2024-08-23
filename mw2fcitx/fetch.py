from http.client import HTTPException
import json
import sys
from json.decoder import JSONDecodeError
from os import access, R_OK, fdopen
from tempfile import mkstemp
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import quote_plus

from .logger import console
from .retry import retry


class StatusError(Exception):

    def __init__(self, code):
        super().__init__(f"HTTP status is {code}")


@retry()
def open_request(url):
    return urlopen(
        Request(
            url,
            headers={
                "User-Agent":
                    "MW2Fcitx/1.0; github.com/outloudvi/fcitx5-pinyin-moegirl"
            }))


def fetch_as_json(url):
    for _ in range(3):
        try:
            res = open_request(url)
            if res.status == 200:
                return json.loads(res.read())
        except (JSONDecodeError, HTTPError) as e:
            console.error(f"Fetch error {str(e)}, retrying")
            continue
    console.error(f"Error fetching URL {url}")
    raise StatusError(res.status)


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
        console.warn(f"Cannot read partial session: {partial_path}")
        return [[], None]
    try:
        partial_data = json.load(open(partial_path, "r", encoding="utf-8"))
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
    fetch_url = api_url + "?action=query&list=allpages&format=json"
    if partial_path is not None:
        console.info(f"Partial session will be saved/read: {partial_path}")
        [titles, apcontinue] = resume_from_partial(partial_path)
        if apcontinue is not None:
            fetch_url = api_url + \
                f"?action=query&list=allpages&format=json&aplimit=max&apcontinue={quote_plus(apcontinue)}"
            console.info(
                f"{len(titles)} titles found. Continuing from {apcontinue}")
    try:
        data = fetch_as_json(fetch_url)
    except (StatusError, HTTPError):
        # It somehow cannot proceed
        if len(titles) == 0:
            raise Exception("Failed to retrieve any title")
        else:
            # Failed during fetching
            [fd, fpath] = mkstemp(prefix="mwf-titles")
            with fdopen(fd, 'w') as f:
                f.write('\n'.join(titles))
            console.error(
                f"Fetch halted due to exceptions. Check '{fpath}' for current progress."
            )
            raise Exception(
                f"Failed during fetching the titles: {len(titles)} fetched and failed at '{apcontinue}'."
            )
    breakNow = False
    while True:
        for i in map(lambda x: x["title"], data["query"]["allpages"]):
            titles.append(i)
            if limit != -1 and len(titles) >= limit:
                breakNow = True
                break
        console.debug(f"Got {len(titles)} pages")
        if breakNow:
            break
        if "continue" in data:
            try:
                apcontinue = data["continue"]["apcontinue"]
                data = fetch_as_json(
                    api_url +
                    f"?action=query&list=allpages&format=json&aplimit=max&apcontinue={quote_plus(apcontinue)}"
                )
            except (HTTPException, TimeoutError, URLError) as e:
                console.error(str(e))
                if partial_path:
                    save_to_partial(partial_path, titles, apcontinue)
                sys.exit(1)
            except KeyboardInterrupt:
                console.error("Keyboard interrupt received. Stopping.")
                if partial_path:
                    save_to_partial(partial_path, titles, apcontinue)
                sys.exit(1)
        else:
            break
    console.info("Finished.")
    return titles
