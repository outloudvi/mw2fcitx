> [!NOTE]
> 如果您需要下载**萌娘百科 (zh.moegirl.org.cn) 词库**，请[参见此页](https://github.com/outloudvi/mw2fcitx/wiki/fcitx5-pinyin-moegirl)。
>
> For the **pre-built dictionary for Moegirlpedia** (zh.moegirl.org.cn), see [the wiki](https://github.com/outloudvi/mw2fcitx/wiki/fcitx5-pinyin-moegirl#extra-dictionaries).

> [!WARNING]
> `mw2fcitx` 0.20.0 包含一些主要和繁简转换相关的 breaking changes。请查看 [BREAKING_CHANGES.md](./BREAKING_CHANGES.md) 了解更多信息。

---

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
# or if you need to use OpenCC for text conversion
pip install mw2fcitx[opencc]
```

## CLI Usage

```
mw2fcitx -c config_script.py
```

## Configuration Script Format

```python
from mw2fcitx.tweaks.moegirl import tweaks
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
            # Deprecated. Please use `source.kwargs.api_params.aplimit` instead. (optional)
            "aplimit": "max",
            # Override ALL parameters while calling MediaWiki API.
            "api_params": {
                # Results per API request; same as `aplimit` in MediaWiki docs. (optional)
                "aplimit": "max"
            }
        }
    },
    # Tweaks configurations as an list.
    # Every tweak function accepts a list of titles and return
    #     a list of title.
    "tweaks":
        tweaks,
    # Converter configurations.
    "converter": {
        # pypinyin is a built-in converter.
        # For custom converter functions, just give the function itself.
        "use": "pypinyin",
        "kwargs": {
            # Replace "m" to "mu" and "n" to "en". Default: False.
            # See more in https://github.com/outloudvi/mw2fcitx/issues/29 .
            "disable_instinct_pinyin": False,
            # Pinyin results to replace. (optional)
            # Format: { "汉字": "pin'yin" }
            "fixfile": "fixfile.json",
            # Characters to omit during pinyin conversion. (optional)
            # These characters will be automatically removed while trying to convert to pinyin.
            # As a result, words containing these characters will not be skipped in the dictionary.
            "characters_to_omit": ["·"],
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

## Advanced mode

As `mw2fcitx` provides the feature to append and override MediaWiki API parameters, it is possible to use it to collect other types of lists in addition to [`allpages`](https://www.mediawiki.org/wiki/Special:MyLanguage/API:Allpages). Please note that if `list`, `action` or `format` is overriden in `api_params`, `mw2fcitx` will not automatically append any default parameter (except for `format`) while sending MediaWiki API requests. Please determine the parameters needed by yourself. [A configuration in tests](tests/cli/confs/conf_list_categorymembers.py) may be helpful for your reference.

## Breaking changes across versions

Read [BREAKING_CHANGES.md](./BREAKING_CHANGES.md) for details.

## License

[MIT License](https://github.com/outloudvi/mw2fcitx/blob/master/LICENSE)
