import time
import pytest

from mw2fcitx.main import inner_main


def test_inner_main_name_without_py():
    inner_main(['-c', 'tests/cli/conf_one'])


def test_inner_main_name_with_py():
    inner_main(['-c', 'tests/cli/conf_one.py'])


def test_single_generator():
    inner_main(['-c', 'tests/cli/conf_single_generator'])


def test_local():
    inner_main(['-c', 'tests/cli/conf_local'])
    with open("test_local_result.dict.yml", "r", encoding="utf-8") as f:
        assert f.read() == """---
name: e2etest_local
version: "0.1"
sort: by_weight
...
初音未来	chu yin wei lai
"""


def test_continue():
    # this should run at least 8 secs = 2 * (5 / 1) - 2
    start = time.perf_counter()
    inner_main(['-c', 'tests/cli/conf_continue'])
    end = time.perf_counter()
    assert end-start > 8


def test_err_no_path():
    with pytest.raises(SystemExit):
        inner_main(['-c', 'tests/cli/conf_err_no_path'])
