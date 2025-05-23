from mw2fcitx.pipeline import MWFPipeline


def test_rime_dict_name():
    pipeline = MWFPipeline()
    pipeline.load_titles(["测试"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="pypinyin")
    pipeline.generate_dict(generator="rime", **{
        "name": "new_name",
        "version": "1.3.5"
    })
    assert pipeline.dict.strip() == """
---
name: new_name
sort: by_weight
version: 1.3.5
...
测试	ce shi
""".strip()


def test_rime_dict_default_name():
    pipeline = MWFPipeline()
    pipeline.load_titles(["测试"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="pypinyin")
    pipeline.generate_dict(generator="rime")
    assert pipeline.dict.strip() == """
---
name: unnamed_dict
sort: by_weight
version: '0.1'
...
测试	ce shi
""".strip()
