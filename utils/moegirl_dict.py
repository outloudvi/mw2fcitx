from mw2fcitx.tweaks.moegirl import tweaks, tweak_opencc_t2s, tweak_replace_characters

exports = {
    "source": {
        "api_path": "https://zh.moegirl.org.cn/api.php",
        "file_path": [
            # "titles.txt",  # use file-based title source for now
            "extras/pcr.txt"
        ],
        "kwargs": {
            "output": "titles.txt"
        }
    },
    "tweaks": tweaks + [
        tweak_opencc_t2s,
        tweak_replace_characters({
            "筿": "篠"
        })
    ],
    "converter": {
        "use": "opencc",
        "kwargs": {
            "fixfile": "fixfile.json"
        }
    },
    "generator": [{
        "use": "rime",
        "kwargs": {
            "name": "moegirl",
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
