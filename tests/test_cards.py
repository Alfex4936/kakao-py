import msgspec
import pytest
from kakao_json import Button, Kakao, ListItem


@pytest.fixture
def k():
    return Kakao()


class TestBasicCard:
    def test_basic_card(self, k):
        k.add_qr("오늘", "카톡 발화문1")
        k.add_qr("어제")  # label becomes also messageText

        list_card = k.init_list_card().set_header("리스트 카드 제목")
        list_card.add_button(Button("그냥 텍스트 버튼", "message"))
        list_card.add_button(k.init_button("link label").set_link("https://google.com"))
        list_card.add_button(
            k.init_button("share label").set_action_share().set_msg("카톡에 보이는 메시지")
        )
        list_card.add_button(k.init_button("call label").set_number("010-1234-5678"))

        list_card.add_item(
            ListItem("title").set_desc("description").set_link("https://naver.com")
        )

        k.add_output(list_card)

        assert (
            b'{"version":"2.0","template":{"outputs":[{"listCard":{"header":{"title":"\xeb\xa6\xac\xec\x8a\xa4\xed\x8a\xb8 \xec\xb9\xb4\xeb\x93\x9c \xec\xa0\x9c\xeb\xaa\xa9"},"items":[{"title":"title","description":"description","link":{"web":"https://naver.com"},"action":"message"}],"buttons":[{"label":"\xea\xb7\xb8\xeb\x83\xa5 \xed\x85\x8d\xec\x8a\xa4\xed\x8a\xb8 \xeb\xb2\x84\xed\x8a\xbc","action":"message"},{"label":"link label","action":"webLink","webLinkUrl":"https://google.com"},{"label":"share label","action":"share","messageText":"\xec\xb9\xb4\xed\x86\xa1\xec\x97\x90 \xeb\xb3\xb4\xec\x9d\xb4\xeb\x8a\x94 \xeb\xa9\x94\xec\x8b\x9c\xec\xa7\x80"},{"label":"call label","action":"phone","phoneNumber":"010-1234-5678"}]}}],"quickReplies":[{"action":"message","label":"\xec\x98\xa4\xeb\x8a\x98","messageText":"\xec\xb9\xb4\xed\x86\xa1 \xeb\xb0\x9c\xed\x99\x94\xeb\xac\xb81"},{"action":"message","label":"\xec\x96\xb4\xec\xa0\x9c","messageText":"\xec\x96\xb4\xec\xa0\x9c"}]}}'
            == k.to_json()
        )
