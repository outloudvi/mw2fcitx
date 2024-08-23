from mw2fcitx.utils import is_libime_used


def test_is_libime_used():
    assert (
        is_libime_used({}) == False
    )

    assert (
        is_libime_used({
            "generator": [{
                "use": "rime",
                "kwargs": {
                    "output": "1.yml"
                }
            }]
        }) == False
    )

    assert (
        is_libime_used({
            "generator": [{
                "use": "rime",
                "kwargs": {
                    "output": "1.yml"
                }
            }, {
                "use": "pinyin",
                "kwargs": {
                    "output": "1.dict"
                }
            }]
        }) == True
    )
