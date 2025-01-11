from os.path import getsize

from mw2fcitx.pipeline import MWFPipeline


def test_pipeline_basic():
    pipeline = MWFPipeline()
    pipeline.load_titles(["测试", "百科", "朝之琉璃"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="opencc",
                          fixfile="mw2fcitx/sample_fixfile.json")
    assert pipeline.exports != ""
    pipeline.generate_dict(generator="rime",
                           output="test.dict.yml",
                           name="test",
                           version="1.0")
    assert getsize("test.dict.yml") > 0
    pipeline.generate_dict(
        generator="pinyin",
        output="test.dict",
    )
    assert getsize("test.dict") > 0
    # pylint: disable=consider-using-with
    assert ("朝之琉璃	zhao zhi liu li" in open('test.dict.yml',
                                           "r",
                                           encoding='utf-8').read())
