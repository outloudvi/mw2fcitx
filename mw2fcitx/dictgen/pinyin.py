import tempfile
import subprocess
from ..utils import console


def gen(text, **kwargs):
    file = tempfile.NamedTemporaryFile("w+")
    file.write(text)
    console.info("Running libime_pinyindict...")
    subprocess.run(["libime_pinyindict", file.name, kwargs["output"]],
                   check=True)
    console.info("Dictionary generated.")
