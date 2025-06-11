import logging
from typing import List, Union
from pypinyin import lazy_pinyin, load_phrases_dict

from ..const import PYPINYIN_KW_CHARACTERS_TO_OMIT, PYPINYIN_KW_DISABLE_INSTINCT_PINYIN

log = logging.getLogger(__name__)

DEFAULT_PLACEHOLDER = "_ERROR_"

# https://github.com/outloudvi/mw2fcitx/issues/29
INSTINCT_PINYIN_MAPPING = {
    "n": "en",
    "m": "mu",
}


def load_phrases(fix_table: dict):
    items = {}
    for (key, value) in fix_table.items():
        phrases = list(map(lambda x: [x], value.split("'")))
        items[key] = phrases
    load_phrases_dict(items)


def export(words: List[Union[dict, str]], **kwargs) -> str:
    disable_instinct_pinyin = kwargs.get(
        PYPINYIN_KW_DISABLE_INSTINCT_PINYIN) is True
    characters_to_omit = kwargs.get(PYPINYIN_KW_CHARACTERS_TO_OMIT, [])

    fix_table = kwargs.get("fix_table") or {}
    load_phrases(fix_table)

    result = ""
    count = 0
    for line in words:
        line = line.rstrip("\n")

        pinyin = None

        line_for_pinyin = line
        if len(characters_to_omit) > 0:
            line_for_pinyin = ''.join(
                [char for char in line_for_pinyin if char not in characters_to_omit])

        if pinyin is None:
            pinyins = lazy_pinyin(
                line_for_pinyin, errors=lambda x: DEFAULT_PLACEHOLDER)
            if not disable_instinct_pinyin:
                pinyins = [INSTINCT_PINYIN_MAPPING.get(x, x) for x in pinyins]
            if DEFAULT_PLACEHOLDER in pinyins:
                # The word is not fully converable
                continue
            pinyin = "'".join(pinyins)
            if pinyin == line:
                # print("Failed to convert, ignoring:", pinyin, file=sys.stderr)
                continue

        result += "\t".join((line, pinyin, "0"))
        result += "\n"
        count += 1
        if count % 1000 == 0:
            log.debug(str(count) + " converted")

    if count % 1000 != 0 or count == 0:
        log.debug(str(count) + " converted")
    return result
