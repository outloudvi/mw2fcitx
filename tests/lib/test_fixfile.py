from mw2fcitx.pipeline import MWFPipeline
from tests.lib.util import get_sorted_word_list


def test_fixfile_with_partial():
    pipeline = MWFPipeline()
    pipeline.load_titles(["测试", "测试二", "刻俄柏", "刻俄柏的灰蕈迷境"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="pypinyin", fix_table={
        "测试": "pin'yin",
        "测试二": {
            "to": "yi'er'san"
        },
        "刻俄柏": {
            "to": "ke'e'bo"
        }
    })
    pipeline.generate_dict(generator="rime")
    assert get_sorted_word_list(pipeline.dict) == """
刻俄柏	ke e bo
刻俄柏的灰蕈迷境	ke e bo de hui xun mi jing
测试	pin yin
测试二	yi er san
""".strip()


def test_fixfile_no_partial():
    pipeline = MWFPipeline()
    pipeline.load_titles(["测试"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="pypinyin", fix_table={
        "测试": "pin'yin"
    })
    pipeline.generate_dict(generator="rime")
    assert pipeline.dict.strip() == """
---
name: unnamed_dict
sort: by_weight
version: '0.1'
...
测试	pin yin
""".strip()
