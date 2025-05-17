# pylint: disable=duplicate-code
from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "api_path": "https://zh.wikipedia.org/w/api.php",
        "kwargs": {
            "title_limit": 50,
            "output": "titles.txt"
        }
    },
    "tweaks":
        tweaks,
    "converter": {
        "use": "opencc",
        "kwargs": {}
    },
    "generator": {
        "use": "rime",
        "kwargs": {
            "output": "moegirl.dict.yml"
        }
    }
}
