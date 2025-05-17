# pylint: disable=duplicate-code
from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "file_path": "tests/cli/test.txt"
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
            "output": "test_local_result.dict.yml"
        }
    }]
}
