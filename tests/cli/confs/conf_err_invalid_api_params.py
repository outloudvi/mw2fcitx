# pylint: disable=duplicate-code

exports = {
    "source": {
        "api_path": "https://zh.wikipedia.org/w/api.php",
        "kwargs": {
            "title_limit": 10,
            "api_params": {
                "action": "paraminfo",
                "modules": "query+allpages"
            },
            "output": "test_err_invalid_api_params.titles.txt"
        }
    },
    "tweaks": [],
    "converter": {
        "use": "opencc",
        "kwargs": {}
    },
    "generator": []
}
