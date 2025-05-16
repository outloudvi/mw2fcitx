# pylint: disable=duplicate-code

exports = {
    "source": {
        "api_path": "https://zh.wikipedia.org/w/api.php",
        "kwargs": {
            "title_limit": 25,
            "api_params": {
                "aplimit": 12
            },
            "output": "test_api_title_limit.titles.txt"
        }
    },
    "tweaks": [],
    "converter": {
        "use": "opencc",
        "kwargs": {}
    },
    "generator": []
}
