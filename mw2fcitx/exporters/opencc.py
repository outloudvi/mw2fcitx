import json
import re
from pypinyin import lazy_pinyin
import opencc
from ..utils import console

DEFAULT_PLACEHOLDER = "_ERROR_"


def manual_fix(text, table):
    if text in table:
        return table[text]
    return None


def export(words, **kwargs):
    result = ""
    converter = opencc.OpenCC('t2s.json')
    fixfile = kwargs.get("fixfile")
    if fixfile is not None:
        table = json.load(open(fixfile, "r", encoding="utf-8"))
    count = 0
    for line in words:
        line = line.rstrip("\n")
        pinyins = lazy_pinyin(line, errors=lambda x: DEFAULT_PLACEHOLDER)
        if DEFAULT_PLACEHOLDER in pinyins:
            # The word is not fully converable
            continue
        pinyin = "'".join(pinyins)
        if pinyin == line:
            # print("Failed to convert, ignoring:", pinyin, file=sys.stderr)
            continue

        if fixfile is not None:
            fixed_pinyin = manual_fix(line, table)
            if fixed_pinyin is not None:
                pinyin = fixed_pinyin
                console.debug(f"Fixing {line} to {pinyin}")

        result += "\t".join((converter.convert(line), pinyin, "0"))
        result += "\n"
        count += 1
        if count % 1000 == 0:
            console.debug(str(count) + " converted")

    if count % 1000 != 0 or count == 0:
        console.debug(str(count) + " converted")
    return result
