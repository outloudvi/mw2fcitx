import tempfile
import subprocess

from ..const import LIBIME_BIN_NAME, LIBIME_REPOLOGY_URL
from ..logger import console


def gen(text, **kwargs):
    with tempfile.NamedTemporaryFile("w+") as file:
        file.write(text)
        console.info(f"Running {LIBIME_BIN_NAME}...")
        try:
            subprocess.run([LIBIME_BIN_NAME, file.name, kwargs["output"]],
                           check=True)
        except FileNotFoundError:
            console.error(
                f"The program \"{LIBIME_BIN_NAME}\" is not found. "
                f"Please install libime: {LIBIME_REPOLOGY_URL}"
            )
            raise
        console.info("Dictionary generated.")
