from mw2fcitx.pipeline import MWFPipeline


def test_non_opencc_t2s():
    pipeline = MWFPipeline()
    pipeline.load_titles(["禮節"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="pypinyin")
    assert pipeline.exports == "禮節\tli'jie\t0\n"
