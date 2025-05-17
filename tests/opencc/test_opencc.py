from mw2fcitx.pipeline import MWFPipeline
from mw2fcitx.tweaks.moegirl import tweak_opencc_t2s


def test_opencc_t2s():
    pipeline = MWFPipeline()
    pipeline.load_titles(["禮節"])
    pipeline.convert_to_words([tweak_opencc_t2s])
    print(pipeline.titles)
    pipeline.export_words(converter="pypinyin")
    assert pipeline.exports == "礼节\tli'jie\t0\n"


def test_dedup():
    pipeline = MWFPipeline()
    pipeline.load_titles(["禮節", "礼节"])
    pipeline.convert_to_words([tweak_opencc_t2s])
    pipeline.export_words(converter="pypinyin")
    assert pipeline.exports == "礼节\tli'jie\t0\n"
