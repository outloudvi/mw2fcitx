# pylint: disable=duplicate-code
from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "kwargs": {
            "title_limit": 50,
            "output": "test_result.txt"
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
            "name": "err_local",
            "output": "err_local.dict.yml"
        }
    }]
}
