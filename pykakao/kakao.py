from __future__ import annotations

from typing import Any, Mapping, Optional, Type

import msgspec

try:
    from .components.common import *
    from .components.cards import *
except:
    from components.common import *
    from components.cards import *
from msgspec import Struct

Card = InnerBasicCard | InnerCommerceCard | InnerListCard | InnerItemCard


class InnerSimpleText(Struct):
    text: str  # MUST


class SimpleText(Struct):
    """text가 500자가 넘는 경우, 500자 이후의 글자는 생략되고 전체 보기 버튼을 통해서 전체 내용을 확인할 수 있습니다."""

    simpleText: InnerSimpleText


class InnerSimpleImage(Struct):
    imageUrl: str  # MUST
    altText: str  # MUST


class SimpleImage(Struct):
    simpleImage: InnerSimpleImage


class InnerCarousel(Struct):
    """# [Carousel](https://i.kakao.com/docs/assets/skill/skill-outputs-carousel-example-1.jpg)

    하나의 케로셀 내에서는 모든 이미지를 동일 크기로 설정해야 합니다.

    즉, 케로셀 내 모든 이미지가 정사각형 (1:1) 혹은 모든 이미지가 와이드형 (2:1)으로 통일되어야 합니다.
    """

    type: str
    items: list[Card]
    header: Optional[CarouselHeader] = None

    def add_card(self, card: Card) -> InnerCarousel:
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


class Carousel(Struct):
    carousel: InnerCarousel


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


Output = SimpleText | SimpleImage | BasicCard | CommerceCard | Carousel


class Outputs(Struct, omit_defaults=True):
    outputs: list[Output] = []
    quickReplies: Optional[list[QuickReply]] = None


class Kakao(Struct):
    version: str = "2.0"
    template: Optional[Outputs] = []
    # context: Optional[ContextControl] = None
    # data: Optional[Mapping[str, Any]] = None

    def add_simple_text(self, text):
        """# SimpleText

        제한: 1000자

        text가 500자가 넘는 경우, 500자 이후의 글자는 생략되고 전체 보기 버튼을 통해서 전체 내용을 확인할 수 있습니다.
        """
        self.outputs.append(SimpleText(InnerSimpleText(text)))

    def add_simple_image(self, url, alt_text):
        """# SimpleImage

        간단한 이미지형 출력 요소입니다.

        이미지 링크 주소를 포함하면 이를 스크랩하여 사용자에게 전달합니다.

        이미지 링크 주소가 유효하지 않을 수 있기 때문에, 대체 텍스트를 꼭 포함해야 합니다.

        ## Parameters

        url: 전달하고자 하는 이미지의 url입니다. URL 형식 (http://)

        alt_text: url이 유효하지 않은 경우, 전달되는 텍스트입니다. 최대 1000자

        """
        self.outputs.append(SimpleImage(InnerSimpleImage(url, alt_text)))

    def init_button(
        self, label: Optional[str] = None, action: Optional[str] = None
    ) -> Button:
        return Button(label=label, action=action)  # type: ignore

    def init_basic_card(self) -> InnerBasicCard:
        """Creates BasicCard instance"""
        return InnerBasicCard()  # type: ignore

    def init_commerce_card(self) -> InnerCommerceCard:
        """Creates CommerceCard instance"""
        return InnerCommerceCard()  # type: ignore

    def init_list_item(self) -> ListItem:
        return ListItem()

    def add_output(self, output):
        match (output.__name__):
            case "CommerceCard":
                self.template.outputs.append(CommerceCard(output))
            case "BasicCard":
                self.template.outputs.append(BasicCard(output))
            case "ListCard":
                self.template.outputs.append(ListCard(output))
            case _:
                self.template.outputs.append(output)

    def to_json(self):
        return msgspec.json.encode(self)


if __name__ == "__main__":
    k = Kakao()
    print(msgspec.json.encode(k.init_button()))
    print(msgspec.json.encode(k.init_button("labell")))
    # k.add_simple_text("hello")
    # k.add_simple_image("https://", "hello")

    basic_card = k.init_basic_card()
    basic_card.set_title("title").set_desc("hello").add_button(
        k.init_button("labell").set_action_web().set_link("https://naver.com")
    )

    k.add_output(basic_card)

    print(msgspec.json.encode(k))

    def matches_default(value: Any, default: Any) -> bool:
        """Whether a value matches the default for a field"""
        if value is default:
            return True
        if type(value) != type(default):
            return False
        if type(value) in (list, set, dict) and (len(value) == len(default) == 0):
            return True
        return False

    print(matches_default(Optional[ContextControl], None))
    print(matches_default(str, "2"))
    print(matches_default(Optional[list[Output]], []))
