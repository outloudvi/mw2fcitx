## Breaking Changes

### 0.20.0

* BREAKING: Like what `file_title_limit` is already doing, `api_title_limit` now also works to trim the title count to the exact limit number.
* BREAKING: The exporter `opencc` is renamed to `pypinyin`. OpenCC-related Traditional/Simplified Chinese conversion is moved to be the `tweak_opencc_t2s` tweak. As a result, `mw2fcitx` will not have a hard dependency on [`opencc`](https://pypi.org/project/OpenCC/). If you need `tweak_opencc_t2s`, you may want to install `mw2fcitx[opencc]` which includes the `opencc` dependency.
* BREAKING: As a result of the change listed above, `tweaks` in `mw2fcitx.tweaks.moegirl` no longer does automatic Traditional/Simplified Chinese conversion.
* Switched to MIT License.

### 0.19.0

* BREAKING: `source.kwargs.aplimit` is moved to `source.kwargs.api_params.aplimit`.

### 0.17.0

* BREAKING: Pinyin "m" will be replaced to "mu" and "n" to "en". To revert the behavior, set `"disable_instinct_pinyin": False` for OpenCC converter. [[#29](https://github.com/outloudvi/mw2fcitx/issues/29)]