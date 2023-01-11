import pytest
from pykakao import kakao
import msgspec


@pytest.fixture
def k():
    return kakao.Kakao()


class TestButton:
    def test_create_button(self, k):
        basic_card = k.init_basic_card()
        basic_card.set_title("title").set_desc("hello").add_button(
            k.init_button("labell").set_action_web().set_link("https://naver.com")
        )

        k.add_output(basic_card)

        assert (
            b'{"outputs":[{"basicCard":{"title":"title","description":"hello","buttons":[{"label":"labell","action":"webLink","webLinkUrl":"https://naver.com"}]}}],"version":"2.0"}'
            == msgspec.json.encode(k)
        )
