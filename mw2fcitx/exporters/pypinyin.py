from typing import List, Union
from pypinyin import lazy_pinyin

from ..const import PYPINYIN_KW_CHARACTERS_TO_OMIT, PYPINYIN_KW_DISABLE_INSTINCT_PINYIN
from ..logger import console

DEFAULT_PLACEHOLDER = "_ERROR_"

# https://github.com/outloudvi/mw2fcitx/issues/29
INSTINCT_PINYIN_MAPPING = {
    "n": "en",
    "m": "mu",
}


def manual_fix(text: str, table: dict) -> Union[str, None]:
    if text in table:
        return table[text]
    return None


def export(words: List[Union[dict, str]], **kwargs) -> str:
    disable_instinct_pinyin = kwargs.get(
        PYPINYIN_KW_DISABLE_INSTINCT_PINYIN) is True
    characters_to_omit = kwargs.get(PYPINYIN_KW_CHARACTERS_TO_OMIT, [])

    result = ""
    fix_table = kwargs.get("fix_table")
    count = 0
    for line in words:
        line = line.rstrip("\n")

        pinyin = None
        if fix_table is not None:
            fixed_pinyin = manual_fix(line, fix_table)
            if fixed_pinyin is not None:
                pinyin = fixed_pinyin
                console.debug(f"Fixing {line} to {pinyin}")

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
            console.debug(str(count) + " converted")

    if count % 1000 != 0 or count == 0:
        console.debug(str(count) + " converted")
    return result
