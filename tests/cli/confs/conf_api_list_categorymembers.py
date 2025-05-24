# pylint: disable=duplicate-code

exports = {
    "source": {
        "api_path": "https://zh.wikipedia.org/w/api.php",
        "kwargs": {
            "title_limit": 10,
            "api_params": {
                "action": "query",
                "list": "categorymembers",
                "cmtitle": "Category:天津市历史风貌建筑",
                "cmlimit": 5
            },
            "output": "test_list_categorymembers.titles.txt"
        }
    },
    "tweaks": [],
    "converter": {
        "use": "opencc",
        "kwargs": {}
    },
    "generator": []
}
