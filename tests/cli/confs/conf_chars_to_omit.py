# pylint: disable=duplicate-code

exports = {
    "source": {
        "file_path": "tests/cli/test.txt",
        "kwargs": {
            "title_limit": 50,
            "output": "test_result.txt"
        }
    },
    "tweaks": [],
    "converter": {
        "use": "pypinyin",
        "kwargs": {
            "characters_to_omit": ["·"]
        }
    },
    "generator": [{
        "use": "rime",
        "kwargs": {
            "name": "e2etest_local",
            "output": "test_chars_to_omit.dict.yml"
        }
    }]
}
