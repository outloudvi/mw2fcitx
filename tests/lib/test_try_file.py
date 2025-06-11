import os
import random
import tempfile

from mw2fcitx.utils import try_file


def test_invalid_py_file():
    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.write(b"invalid")
    tmpfile.close()
    assert try_file(tmpfile.name) is False


def test_unreadable_file():
    rnd_filename = f"{random.random()}.rnd"
    for i in range(3):
        if not os.access(rnd_filename, os.R_OK):
            break
        if i == 2:
            # Let's just return if I cannot find a unreadable file
            return
        rnd_filename = f"{random.random()}.rnd"
    assert try_file(rnd_filename) is False
