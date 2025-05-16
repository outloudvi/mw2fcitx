## Breaking Changes

### 0.19.0

* BREAKING: `source.kwargs.aplimit` is moved to `source.kwargs.api_params.aplimit`.

### 0.17.0

* BREAKING: Pinyin "m" will be replaced to "mu" and "n" to "en". To revert the behavior, set `"disable_instinct_pinyin": False` for OpenCC converter. [[#29](https://github.com/outloudvi/mw2fcitx/issues/29)]