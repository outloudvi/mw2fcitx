# pylint: disable=duplicate-code
from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "api_path": "https://zh.wikipedia.org/w/api.php",
        "kwargs": {
            "title_limit": 20,
            "api_params": {
                "apnamespace": 4,
                "apprefix": "《求闻》/2019年第1卷"
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
            "name": "e2etest_local",
            "output": "test_api_params.dict.yml"
        }
    }]
}
