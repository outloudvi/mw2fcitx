import os
import pytest
from requests.exceptions import ProxyError


def test_http_proxy():
    old_value = os.environ.get("HTTPS_PROXY")

    os.environ["HTTPS_PROXY"] = "http://127.0.0.1:39999"
    from mw2fcitx.pipeline import MWFPipeline
    pipeline = MWFPipeline("https://zh.wikipedia.org/w/api.php")
    with pytest.raises(ProxyError):
        pipeline.fetch_titles(title_limit=50)

    if old_value is not None:
        os.environ["HTTPS_PROXY"] = old_value
    else:
        del os.environ["HTTPS_PROXY"]
