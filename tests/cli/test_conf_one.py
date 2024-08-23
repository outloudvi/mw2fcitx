from mw2fcitx.main import inner_main


def test_inner_main_name_without_py():
    inner_main(['-c', 'tests/cli/conf_one'])


def test_inner_main_name_with_py():
    inner_main(['-c', 'tests/cli/conf_one.py'])
