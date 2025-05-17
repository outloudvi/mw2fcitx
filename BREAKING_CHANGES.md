## Breaking Changes

### 0.20.0

* BREAKING: Like what `file_title_limit` is already doing, `api_title_limit` now also works to trim the title count to the exact limit number.
* Switched to MIT License.

### 0.19.0

* BREAKING: `source.kwargs.aplimit` is moved to `source.kwargs.api_params.aplimit`.

### 0.17.0

* BREAKING: Pinyin "m" will be replaced to "mu" and "n" to "en". To revert the behavior, set `"disable_instinct_pinyin": False` for OpenCC converter. [[#29](https://github.com/outloudvi/mw2fcitx/issues/29)]