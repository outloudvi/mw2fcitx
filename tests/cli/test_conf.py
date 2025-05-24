import time
import pytest

from mw2fcitx.main import inner_main
from tests.lib.util import requires_real_world


def get_sorted_word_list(content: str) -> str:
    return "\n".join(sorted(content.split("\n")[5:])).strip()


def test_inner_main_name_without_py():
    inner_main(['-c', 'tests/cli/confs/conf_local'])


def test_inner_main_name_with_py():
    inner_main(['-c', 'tests/cli/confs/conf_local.py'])


def test_local():
    inner_main(['-c', 'tests/cli/confs/conf_local'])
    with open("test_local_result.dict.yml", "r", encoding="utf-8") as f:
        assert get_sorted_word_list(f.read()) == """
初音未来	chu yin wei lai
迈克杰克逊	mai ke jie ke xun""".strip()


def test_chars_to_omit():
    inner_main(['-c', 'tests/cli/confs/conf_chars_to_omit'])
    with open("test_chars_to_omit.dict.yml", "r", encoding="utf-8") as f:
        assert get_sorted_word_list(f.read()) == """
初音未来	chu yin wei lai
迈克·杰克逊	mai ke jie ke xun""".strip()


def test_err_no_path():
    with pytest.raises(SystemExit):
        inner_main(['-c', 'tests/cli/confs/conf_err_no_path'])


@requires_real_world()
def test_api_err_invalid_params():
    with pytest.raises(SystemExit):
        inner_main(['-c', 'tests/cli/confs/conf_api_err_invalid_params'])


@requires_real_world()
def test_api_continue():
    # this should run at least 8 secs = 2 * (5 / 1) - 2
    start = time.perf_counter()
    inner_main(['-c', 'tests/cli/confs/conf_api_continue'])
    end = time.perf_counter()
    assert end-start > 8


@requires_real_world()
def test_api_params():
    inner_main(['-c', 'tests/cli/confs/conf_api_params'])
    with open("test_api_params.dict.yml", "r", encoding="utf-8") as f:
        assert get_sorted_word_list(f.read()) == """
专题关注	zhuan ti guan zhu
全域动态	quan yu dong tai
本地社群新闻	ben di she qun xin wen""".strip()


@requires_real_world()
def test_api_title_limit():
    inner_main(['-c', 'tests/cli/confs/conf_api_title_limit'])
    with open("test_api_title_limit.titles.txt", "r", encoding="utf-8") as f:
        assert len(f.read().split("\n")) == 25


@requires_real_world()
def test_api_list_categorymembers():
    inner_main(['-c', 'tests/cli/confs/conf_api_list_categorymembers'])
    with open("test_list_categorymembers.titles.txt", "r", encoding="utf-8") as f:
        assert len(f.read().split("\n")) == 10
