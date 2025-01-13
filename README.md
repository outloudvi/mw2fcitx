# mw2fcitx

Build fcitx5/RIME dictionaries from MediaWiki sites.

[![PyPI](https://img.shields.io/pypi/v/mw2fcitx)](https://pypi.org/project/mw2fcitx/)
[![Tests](https://github.com/outloudvi/mw2fcitx/actions/workflows/test.yml/badge.svg)](https://github.com/outloudvi/mw2fcitx/actions/workflows/test.yml)
[![codecov: Coverage](https://codecov.io/gh/outloudvi/mw2fcitx/graph/badge.svg?token=1RP1099913)](https://codecov.io/gh/outloudvi/mw2fcitx)

```sh
pip install mw2fcitx
# or if you want to just install for current user
pip install mw2fcitx --user
# or if you want to just run it (needs Pipx)
pipx run mw2fcitx
```

For the pre-built moegirl dictionary info, see [the wiki](https://github.com/outloudvi/mw2fcitx/wiki/fcitx5-pinyin-moegirl).

## CLI Usage

```
mw2fcitx -c config_script.py
```

## Configuration Script Format

```python
# By default we assume the configuration is located at a variable
#     called "exports".
# You can change this with `-n any_name` in the CLI.

exports = {
    # Source configurations.
    "source": {
        # MediaWiki api.php path, if to fetch titles from online.
        "api_path": "https://zh.moegirl.org.cn/api.php",
        # Title file path, if to fetch titles from local file. (optional)
        # Can be a path or a list of paths.
        "file_path": ["titles.txt"],
        "kwargs": {
            # Title number limit for fetching. (optional)
            "title_limit": 120,
            # Title number limit for fetching via API. (optional)
            # Overrides title_limit.
            "api_title_limit": 120,
            # Title number limit for each fetch via file. (optional)
            # Overrides title_limit.
            "file_title_limit": 60,
            # Partial session file on exception (optional)
            "partial": "partial.json",
            # Title list export path. (optional)
            "output": "titles.txt",
            # Delay between MediaWiki API requests in seconds. (optional)
            "request_delay": 2,
            # Results per API request; same as `aplimit` in MediaWiki docs. (optional)
            "aplimit": "max"
        }
    },
    # Tweaks configurations as an list.
    # Every tweak function accepts a list of titles and return
    #     a list of title.
    "tweaks":
        tweaks,
    # Converter configurations.
    "converter": {
        # opencc is a built-in converter.
        # For custom converter functions, just give the function itself.
        "use": "opencc",
        "kwargs": {
            # Replace "m" to "mu" and "n" to "en". Default: False.
            # See more in https://github.com/outloudvi/mw2fcitx/issues/29 .
            "disable_instinct_pinyin": False,
            # Pinyin results to replace. (optional)
            # Format: { "汉字": "pin'yin" }
            "fixfile": "fixfile.json"
        }
    },
    # Generator configurations.
    "generator": [{
        # rime is a built-in generator.
        # For custom generator functions, just give the function itself.
        "use": "rime",
        "kwargs": {
            # Destination dictionary filename. (optional)
            "output": "moegirl.dict.yml"
        }
    }, {
        # pinyin is a built-in generator.
        # This generator depends on `libime`.
        "use": "pinyin",
        "kwargs": {
            # Destination dictionary filename. (mandatory)
            "output": "moegirl.dict"
        }
    }]
}
```

A sample config file is here: [`sample_config.py`](https://github.com/outloudvi/mw2fcitx/blob/master/mw2fcitx/sample_config.py)

## Breaking changes across versions

Read [BREAKING_CHANGES.md](./BREAKING_CHANGES.md) for details.

## License

[The Unlicense](https://github.com/outloudvi/mw2fcitx/blob/master/LICENSE)
