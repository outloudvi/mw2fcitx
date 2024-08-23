from mw2fcitx.pipeline import MWFPipeline
from mw2fcitx.tweaks.moegirl import tweaks as moegirl_tweaks


def test_pipeline_basic():
    pipeline = MWFPipeline("https://zh.wikipedia.org/w/api.php")
    pipeline.fetch_titles(title_limit=50)
    pipeline.convert_to_words(moegirl_tweaks)
    pipeline.export_words()
    pipeline.generate_dict(generator="rime")
