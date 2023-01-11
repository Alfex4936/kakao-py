import msgspec
import pytest
from kakao_json import Kakao


@pytest.fixture
def k():
    return Kakao()


class TestButton:
    def test_create_button(self, k):
        basic_card = k.init_basic_card()
        basic_card.set_title("title").set_desc("hello").add_button(
            k.init_button("labell").set_action_web().set_link("https://naver.com")
        )

        k.add_output(basic_card)

        assert (
            b'{"version":"2.0","template":{"outputs":[{"basicCard":{"title":"title","description":"hello","buttons":[{"label":"labell","action":"webLink","webLinkUrl":"https://naver.com"}]}}]}}'
            == msgspec.json.encode(k)
        )
