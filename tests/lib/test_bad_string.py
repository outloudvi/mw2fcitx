from mw2fcitx.pipeline import MWFPipeline


def test_bad_string():
    pipeline = MWFPipeline()
    pipeline.load_titles(["__INVALID__CHAR__"])
    pipeline.convert_to_words([])
    pipeline.export_words(converter="pypinyin")
    assert pipeline.exports == ""
