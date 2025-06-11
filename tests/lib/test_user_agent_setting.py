import random
from mw2fcitx.utils import create_requests_session


def test_user_agent_setting():
    rnd = random.random()
    user_agent = f"rnd/{rnd}"
    s = create_requests_session(user_agent)
    assert s.headers.get("User-Agent") == user_agent


def test_null_user_agent_setting():
    s = create_requests_session(None)
    assert "MW2Fcitx" in str(s.headers.get("User-Agent"))
