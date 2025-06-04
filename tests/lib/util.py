import os
import pytest

REAL_WORLD_ENV_NAME = "TEST_REAL_WORLD"


def requires_real_world():
    real_world_test_flag = os.environ.get(REAL_WORLD_ENV_NAME) or "false"

    return pytest.mark.skipif(
        real_world_test_flag.lower() != "true",
        reason=f"Skipping real-world test as ${REAL_WORLD_ENV_NAME} is not `true`"
    )


def get_sorted_word_list(content: str) -> str:
    return "\n".join(sorted(content.split("\n")[5:])).strip()
