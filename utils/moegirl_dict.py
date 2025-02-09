from mw2fcitx.tweaks.moegirl import tweaks

exports = {
    "source": {
        "file_path": [
            "titles.txt",
            "extras/pcr.txt"
        ],
        "kwargs": {
            "output": "titles.txt"
        }
    },
    "tweaks":
        tweaks,
    "converter": {
        "use": "opencc",
        "kwargs": {
            "fixfile": "fixfile.json"
        }
    },
    "generator": [{
        "use": "rime",
        "kwargs": {
            "version": "0.0.1",
            "output": "moegirl.dict.yaml"
        }
    }, {
        "use": "pinyin",
        "kwargs": {
            "output": "moegirl.dict"
        }
    }]
}
