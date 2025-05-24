# pylint: disable=duplicate-code
from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "api_path": "https://zh.wikipedia.org/w/api.php",
        "kwargs": {
            "request_delay": 2,
            "title_limit": 5,  # to test the paginator
            "api_params": {
                "aplimit": 1,
            },
            "output": "titles.txt"
        }
    },
    "tweaks":
        tweaks,
    "converter": {
        "use": "opencc",
        "kwargs": {}
    },
    "generator": [{
        "use": "rime",
        "kwargs": {
            "output": "moegirl.dict.yml"
        }
    }, {
        "use": "pinyin",
        "kwargs": {
            "output": "moegirl.dict"
        }
    }]
}
