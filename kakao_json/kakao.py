from __future__ import annotations

from typing import Any, Mapping, Optional, Type

import msgspec

try:
    from .components.cards import *
    from .components.common import *
except:
    from components.common import *
    from components.cards import *

from msgspec import Struct, field

Card = BasicCard | CommerceCard | ListCard | ItemCard


class SimpleText(Struct):
    text: str  # MUST


class OuterSimpleText(Struct):
    """text가 500자가 넘는 경우, 500자 이후의 글자는 생략되고 전체 보기 버튼을 통해서 전체 내용을 확인할 수 있습니다."""

    simpleText: SimpleText


class SimpleImage(Struct):
    imageUrl: str  # MUST
    altText: str  # MUST


class OuterSimpleImage(Struct):
    simpleImage: SimpleImage


class Carousel(Struct, omit_defaults=True):
    """# [Carousel](https://i.kakao.com/docs/assets/skill/skill-outputs-carousel-example-1.jpg)

    하나의 케로셀 내에서는 모든 이미지를 동일 크기로 설정해야 합니다.

    즉, 케로셀 내 모든 이미지가 정사각형 (1:1) 혹은 모든 이미지가 와이드형 (2:1)으로 통일되어야 합니다.
    """

    __name__ = "Carousel"

    type: str = ""  # MUST
    items: list[Card] = []  # MUST
    header: Optional[CarouselHeader] = None

    def add_card(self, card: Card) -> Carousel:
        match (card.__name__):
            case "BasicCard":
                self.type = "basicCard"
            case "CommerceCard":
                self.type = "commerceCard"
            case "ListCard":
                self.type = "listCard"
            case "ItemCard":
                self.type = "itemCard"
            case _:
                raise Exception("Unknown Card type")

        self.items.append(card)
        return self


class OuterCarousel(Struct):
    carousel: Carousel


class QuickReply(Struct, omit_defaults=True):
    """# [QuickReply](https://i.kakao.com/docs/assets/skill/skill-quickreplies-example-02.png)

    바로가기 응답은 발화와 동일합니다.

    대신, 사용자가 직접 발화를 입력하지 않아도 선택을 통해서 발화를 전달하거나 다른 블록을 호출할 수 있습니다.

    제한적 선택지를 가진 응답이거나, 다음 발화에 대한 힌트를 줄 필요가 있을 때 바로가기 응답을 사용하면 유용합니다.
    """

    action: str  # message | block
    label: str
    messageText: str
    blockId: Optional[str] = None
    extra: Optional[Any] = None


Output = (
    OuterSimpleText
    | OuterSimpleImage
    | OuterBasicCard
    | OuterCommerceCard
    | OuterCarousel
)


class Outputs(Struct, omit_defaults=True):
    outputs: list[Output] = field(default_factory=list)
    quickReplies: Optional[list[QuickReply]] = field(default_factory=list)


class Kakao(Struct):
    version: str = "2.0"
    template: Optional[Outputs] = field(default_factory=Outputs) # type: ignore
    # context: Optional[ContextControl] = None
    # data: Optional[Mapping[str, Any]] = None
    
    def clear(self):
        """Reset all template outputs"""
        self.template = Outputs()

    def add_qr(
        self, label: str, messageText: Optional[str] = None, action: str = "message"
    ):
        """Add Quick reply (label, messageText (optional), action)"""
        self.template.quickReplies.append(
            QuickReply(action, label, label if messageText is None else messageText)
        )

    def add_simple_text(self, text):
        """# SimpleText

        제한: 1000자

        text가 500자가 넘는 경우, 500자 이후의 글자는 생략되고 전체 보기 버튼을 통해서 전체 내용을 확인할 수 있습니다.
        """
        self.template.outputs.append(OuterSimpleText(SimpleText(text)))

    def simple_text(self, text):
        """Same as add_simple_text"""
        return self.add_simple_text(text)  # type: ignore

    def add_simple_image(self, url, alt_text):
        """# SimpleImage

        간단한 이미지형 출력 요소입니다.

        이미지 링크 주소를 포함하면 이를 스크랩하여 사용자에게 전달합니다.

        이미지 링크 주소가 유효하지 않을 수 있기 때문에, 대체 텍스트를 꼭 포함해야 합니다.

        ## Parameters

        url: 전달하고자 하는 이미지의 url입니다. URL 형식 (http://)

        alt_text: url이 유효하지 않은 경우, 전달되는 텍스트입니다. 최대 1000자

        """
        self.template.outputs.append(OuterSimpleImage(SimpleImage(url, alt_text)))

    def init_button(
        self, label: Optional[str] = None, action: Optional[str] = None
    ) -> Button:
        return Button(label=label, action=action)  # type: ignore

    def init_basic_card(self) -> BasicCard:
        """Creates BasicCard instance"""
        return BasicCard()  # type: ignore

    def init_commerce_card(self) -> CommerceCard:
        """Creates CommerceCard instance"""
        return CommerceCard()  # type: ignore

    def init_list_card(self) -> ListCard:
        """Creates ListCard instance"""
        return ListCard()  # type: ignore

    def init_list_item(self) -> ListItem:
        return ListItem()

    def init_carousel(self) -> Carousel:
        """Creates Carousel instance"""
        return Carousel()

    def add_output(self, output):
        match (output.__name__):
            case "CommerceCard":
                self.template.outputs.append(OuterCommerceCard(output))
            case "BasicCard":
                self.template.outputs.append(OuterBasicCard(output))
            case "ListCard":
                self.template.outputs.append(OuterListCard(output))
            case _:
                self.template.outputs.append(output)

    # def enc_hook(self, obj: Any) -> Any:
    #     if isinstance(obj, Kakao):
    #         return msgspec.json.encode(k)
    #     else:
    #         raise TypeError(f"Objects of type {type(obj)} are not supported")

    def to_json(self):
        return msgspec.json.encode(self)

    def __str__(self) -> str:
        return msgspec.json.encode(self).decode(encoding="utf-8")

    def __repr__(self) -> str:
        return msgspec.json.encode(self).decode(encoding="utf-8")


if __name__ == "__main__":
    k = Kakao()

    k.add_qr("오늘", "카톡 발화문1")
    k.add_qr("어제")  # label becomes also messageText

    list_card = k.init_list_card().set_header("리스트 카드 제목")
    list_card.add_button(Button("그냥 텍스트 버튼", "message"))  # direct call Button
    list_card.add_button(k.init_button("link label").set_link("https://google.com"))
    list_card.add_button(
        k.init_button("share label").set_action_share().set_msg("카톡에 보이는 메시지")
    )
    list_card.add_button(k.init_button("call label").set_number("010-1234-5678"))

    list_card.add_item(
        ListItem("title").set_desc("description").set_link("https://naver.com")
    )

    k.add_output(list_card)

    print(k.to_json())

    a = Kakao()
    a.add_qr("Quick reply")

    carousel = a.init_carousel()
    for i in range(5):
        basic_card = a.init_basic_card()
        basic_card.set_title(f"Hey {i}").set_image("https://kakao")
        carousel.add_card(basic_card)
    a.add_output(carousel)
    print(a)
