import json
from urllib.request import Request, urlopen
from urllib.parse import quote_plus
from utils import console
from retry import retry


class StatusError(Exception):

    def __init__(self, code):
        super().__init__("HTTP status is {}".format(code))


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
    res = open_request(url)
    if res.status == 200:
        return json.loads(res.read())
    console.error("Error fetching URL {}".format(url))
    raise StatusError(res.status)


def fetch_all_titles(api_url, **kwargs):
    limit = kwargs.get("title_limit") or -1
    console.debug("Fetching titles from {}".format(api_url) +
                  (" with a limit of {}".format(limit) if limit != -1 else ""))
    titles = []
    data = fetch_as_json(api_url + "?action=query&list=allpages&format=json")
    breakNow = False
    while True:
        for i in map(lambda x: x["title"], data["query"]["allpages"]):
            titles.append(i)
            if limit != -1 and len(titles) >= limit:
                breakNow = True
                break
        console.debug("Got {} pages".format(len(titles)))
        if breakNow:
            break
        if "continue" in data:
            data = fetch_as_json(
                api_url +
                "?action=query&list=allpages&format=json&aplimit=max&apcontinue={}"
                .format(quote_plus(data["continue"]["apcontinue"])))
        else:
            break
    console.info("Finished.")
    return titles
