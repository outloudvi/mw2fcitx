from mw2fcitx.utils import is_libime_used, sanitize, smart_rewrite


def test_is_libime_used():
    assert (
        is_libime_used({}) is False
    )

    assert (
        is_libime_used({
            "generator": [{
                "use": "rime",
                "kwargs": {
                    "output": "1.yml"
                }
            }]
        }) is False
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
        }) is True
    )


def test_sanitize():
    def test():
        pass
    assert (
        sanitize(test) == "[func test]"
    )

    assert sanitize(lambda x: x) == "[func <lambda>]"

    assert (sanitize({
        "a": [1, "b"],
        "c": {
            "d": None
        }
    }) == {
        "a": ['1', "b"],
        "c": {
            "d": "[<class 'NoneType'>]"
        }
    })


def test_smart_rewrite():
    assert (
        smart_rewrite(
            {
                "generator": [],
                "source": {
                    "file_path": []
                }
            }
        ) == {
            "generator": [],
            "source": {
                "file_path": []
            }
        }
    )

    assert (
        smart_rewrite(
            {
                "generator": {
                    "use": "rime",
                    "kwargs": {
                        "output": "moegirl.dict.yml"
                    }
                },
                "source": {
                    "file_path": []
                }
            }
        ) == {
            "generator": [{
                "use": "rime",
                "kwargs": {
                    "output": "moegirl.dict.yml"
                }
            }],
            "source": {
                "file_path": []
            }
        }
    )

    assert (
        smart_rewrite(
            {
                "generator": [],
                "source": {
                    "file_path": "1.txt"
                }
            }
        ) == {
            "generator": [],
            "source": {
                "file_path": ["1.txt"]
            }
        }
    )
