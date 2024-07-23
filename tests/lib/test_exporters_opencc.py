from mw2fcitx.exporters.opencc import export


def test_opencc_exporter():
    assert (
        export(["测试"]) == "测试\tce'shi\t0\n"
    )

    assert (
        export([
            "测试",
            "琴吹䌷"  # outloudvi/mw2fcitx#16
        ]) == "测试\tce'shi\t0\n"
        "琴吹䌷\tqin'chui'chou\t0\n"
    )

    assert (
        export([
            "测试",
            "无效:词条"
        ]) == "测试\tce'shi\t0\n"

    )


if __name__ == "__main__":
    test_opencc_exporter()
