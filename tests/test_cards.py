import pytest
from pykakao import kakao
import msgspec


@pytest.fixture
def k():
    return kakao.Kakao()


class TestBasicCard:
    def test_basic_card(self, k):
        assert b'{"label":null,"action":null}' == msgspec.json.encode(k.init_button())
        assert b'{"label":"labell","action":null}' == msgspec.json.encode(
            k.init_button("labell")
        )
        assert b'{"label":"labell","action":"webLinkUrl"}' == msgspec.json.encode(
            k.init_button("labell", "webLinkUrl")
        )
