from __future__ import annotations

from typing import Optional

from msgspec import Struct

try:
    from .common import *
except:
    from common import *

__all__ = [
    "OuterBasicCard",
    "BasicCard",
    "OuterCommerceCard",
    "CommerceCard",
    "OuterListCard",
    "ListCard",
    "OuterItemCard",
    "ItemCard",
]


class BasicCard(Struct, omit_defaults=True):
    """# BasicCard

    ## Attributes:
        - title: String, 케로셀 헤드 제목
            - 최대 2줄 (한 줄에 들어갈 수 있는 글자 수는 기기에 따라 달라집니다.)

        - description: String, 케로셀 헤드 설명
            - 최대 3줄 (한 줄에 들어갈 수 있는 글자 수는 기기에 따라 달라집니다.)

        - thumbnail: String, 케로셀 헤드 배경 이미지
            - 현재 imageUrl 값만 지원합니다.
    """

    __name__ = "BasicCard"

    title: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[Thumbnail] = None
    profile: Optional[Profile] = None  # Unsupported API
    social: Optional[Social] = None  # Unsupported API
    buttons: Optional[list[Button]] = []
    forwardable: Optional[bool] = None  # 말풍선에 전달하기 아이콘을 노출합니다.

    def set_title(self, title: str) -> BasicCard:
        self.title = title
        return self

    def set_desc(self, desc: str) -> BasicCard:
        self.description = desc
        return self

    def set_image(self, url: str) -> BasicCard:
        """Create a thumbnail only with image url"""
        self.thumbnail = Thumbnail(url)
        return self

    def set_thumbnail(self, thumbnail: Thumbnail) -> BasicCard:
        self.thumbnail = thumbnail
        return self

    def add_button(self, button: Button) -> BasicCard:
        self.buttons.append(button)  # type: ignore
        return self


class OuterBasicCard(Struct):
    basicCard: BasicCard


class CommerceCard(Struct, omit_defaults=True):
    """# CommerceCard

    ## price, discount, discountedPrice 의 동작 방식

    discountedPrice 가 존재하면 price, discount, discountRate 과 관계 없이 무조건 해당 값이 사용자에게 노출됩니다.
    예) price: 10000, discount: 7000, discountedPrice: 2000 인 경우, 3000 (10000 - 7000)이 아닌 2000이 사용자에게 노출

    위의 예에서 discountedPrice가 없는 경우, 3000이 사용자에게 노출
    예) price: 10000, discountRate: 70, discountedPrice: 2000 인 경우, 3000 (10000 * 0.3)이 아닌 2000이 사용자에게 노출

    discountRate은 discountedPrice를 필요로 합니다. discountedPrice가 주어지지 않으면 사용자에게 >discountRate을 노출하지 않습니다.

    discountRate과 discount가 동시에 있는 경우, discountRate을 우선적으로 노출합니다.

    ## Attributes:
        - description: String, 제품에 대한 상세 설명입니다.
            - 최대 76자

        - price: int, 제품의 가격입니다.

        - currency: String, 제품의 가격에 대한 통화입니다.
            - 현재 won만 가능

        - discount: int, 제품의 가격에 대한 할인할 금액입니다.
        - discountRate: int, 제품의 가격에 대한 할인율입니다.
        - dicountedPrice: int, 제품의 가격에 대한 할인가(할인된 가격)입니다.
        - thumbnails: Array<Thumbnail>, 제품에 대한 사진입니다.
                - 현재 1개만 가능
        - profile: Profile, 제품을 판매하는 프로필 정보입니다.
        - buttons: Array<Button>, 다양한 액션을 수행할 수 있는 버튼입니다.
                - 1개 이상, 3개 이하
    """

    __name__ = "CommerceCard"

    description: str
    price: int  # 말풍선에 전달하기 아이콘을 노출합니다.
    currency: str  # 말풍선에 전달하기 아이콘을 노출합니다.
    discount: Optional[int] = None  # 말풍선에 전달하기 아이콘을 노출합니다.
    discountRate: Optional[int] = None  # 말풍선에 전달하기 아이콘을 노출합니다.
    dicountedPrice: Optional[int] = None  # 말풍선에 전달하기 아이콘을 노출합니다.
    thumbnails: list[Thumbnail] = []
    profile: Optional[Profile] = None
    buttons: list[Button] = []

    def set_price(self, price: int) -> CommerceCard:
        self.price = price
        return self

    def set_desc(self, desc: str) -> CommerceCard:
        self.description = desc
        return self

    def set_currency(self, currency: str) -> CommerceCard:
        if currency != "won":
            raise Exception("Currently only supports 'won'")
        self.currency = currency
        return self

    def set_thumbnail(self, thumbnail: Thumbnail) -> CommerceCard:
        self.thumbnails.append(thumbnail)
        return self

    def add_button(self, button: Button) -> CommerceCard:
        self.buttons.append(button)  # type: ignore
        return self

    def set_discount(self, discount: int) -> CommerceCard:
        self.discount = discount
        return self

    def set_discount_rate(self, rate: int) -> CommerceCard:
        self.discountRate = rate
        return self

    def set_discounted_price(self, sale_price: int) -> CommerceCard:
        self.dicountedPrice = sale_price
        return self


class OuterCommerceCard(Struct):
    commerceCard: CommerceCard


class ListCard(Struct, omit_defaults=True):
    """# ListCard

    리스트 카드형 출력 요소입니다.
    리스트 카드는 표현하고자 하는 대상이 다수일 때, 이를 효과적으로 전달할 수 있습니다.
    헤더와 아이템을 포함하며, 헤더는 리스트 카드의 상단에 위치합니다.
    리스트 상의 아이템은 각각의 구체적인 형태를 보여주며, 제목과 썸네일, 상세 설명을 포함합니다.

    ## Attributes:
        - header: ListItem, 카드의 상단 항목

        - items: Array<ListItem>, 카드의 각각 아이템
            - 최대 5개

        - buttons: Array<Button>
            - 최대 2개
    """

    __name__ = "ListCard"

    header: Optional[ListItem] = None
    items: list[ListItem] = []
    buttons: list[Button] = []

    def set_header(self, title: str) -> ListCard:
        self.header = ListItem(title)
        return self

    def add_item(self, item: ListItem, *items: list[ListItem]) -> ListCard:
        self.items.append(item)
        if items:
            self.items.extend(items)
        return self

    def add_button(self, button: Button) -> ListCard:
        self.buttons.append(button)  # type: ignore
        return self


class OuterListCard(Struct):
    listCard: ListCard


class ImageTitle(Struct):
    """# ImageTitle

    For ItemCard

    ## Attributes:
        - title: String, 이미지타이틀의 제목 정보입니다.
            - 최대 2줄 (한 줄에 들어갈 수 있는 글자수는 기기 별로 상이)
        - description: String, 이미지타이틀의 설명 정보입니다.
            - 최대 1 줄 (한 줄에 들어갈 수 있는 글자수는 기기 별로 상이)
        - imageUrl: String, 이미지타이틀의 이미지 URL입니다.
            - 최적이미지 사이즈 iOS 108 x 108, 안드로이드 98 x 98 (맞지 않는 경우 센터크롭됨)
    """

    title: str
    description: Optional[str]
    imageUrl: Optional[str]


class ItemList(Struct):
    """# ItemList

    For ItemCard

    ## Attributes:
        - title: String, 아이템 제목 정보입니다.
            - 최대 6자
        - description: String, 아이템 설명 정보입니다.
            - 최대 2 줄 (한 줄에 들어갈 수 있는 글자수는 기기 별로 상이)
    """

    title: str
    description: str


class ItemListSummary(Struct):
    """# ItemListSummary

    For ItemCard

    ## Attributes:
        - title: String, 아이템리스트 전체에 대한 제목 정보입니다.
            - 최대 6자
        - description: String, 아이템리스트 전체에 대한 설명 정보입니다.
            - 최대 14자 (통화기호/문자, 숫자, 콤마, 소수점, 띄어쓰기 포함)
                - 문자는 통화 문자만 사용 가능
                - 소수점 두자리까지 사용 가능
    """

    title: str
    description: str


class Head(Struct):
    """# Head

    For ItemCard

    ## Attributes:
        - title: String, 헤드의 타이틀 정보입니다.
            - 최대 1 줄 (한 줄에 들어갈 수 있는 글자수는 기기 별로 상이)
    """

    title: str


class ItemCard(Struct, omit_defaults=True):
    """# [ListCard](https://i.kakao.com/docs/assets/skill/%EC%95%84%EC%9D%B4%ED%85%9C%EB%8B%A8%EC%9D%BC.png)

    itemCard (아이템 말풍선)는 메시지 목적에 따른 유관 정보들을 (가격 정보 포함) 사용자에게 일목요연한 리스트 형태로 전달할 수 있습니다.

    itemCard는 아이템리스트, 제목, 설명 외에 썸네일, 프로필, 헤드, 이미지타이틀, 버튼 그룹을 추가로 포함합니다.

    케로셀 형태로 itemCard를 구현하기 위해서는 [Carousel 도움말](https://i.kakao.com/docs/skill-response-format#carousel)을 함께 참조해주세요.

    ## [Warning](https://i.kakao.com/docs/assets/skill/01_%EC%BC%80%EB%A1%9C%EC%85%80%EA%B7%9C%EC%B9%99%EC%84%A4%EB%AA%85%EC%9D%B4%EB%AF%B8%EC%A7%80.png)

    도움말에서 제공하는 제한 및 유의사항을 확인 및 준수하여 말풍선을 구성해주시길 바랍니다.

    이에 맞지 않게 말풍선을 사용하는 경우, 말풍선이 정상적으로 발송되지 않거나 챗봇 이용제한이 이루어질 수 있습니다.

        - itemCard에서 itemList는 필수 항목입니다.
        - itemCard는 Event API 광고성 메시지로 사용 가능하며, 기존 광고성 말풍선 제한사항을 동일하게 준수하는 경우 정상적으로 발송됩니다.
        - itemCard 케로셀형은 최대 10개의 카드를 구성할 수 있습니다.
        - itemCard 케로셀형에서는 thumbnail, head, profile, imageTitle 필드에 한해 몇몇 케로셀 카드에만 필드를 선택 적용하는 것이 불가능하며 일괄 적용해야 합니다. 다음 이미지를 참고해주세요.

    ## Attributes:
        - itemList: 아이템 목록 정보입니다.
            - 좌측 정렬 디폴트
            - 단일형: 최대 10개까지 사용 가능
            - 케로셀형: 최대 5개까지 사용 가능

        ---

        - thumbnail: Thumbnail, 상단 이미지입니다.
            - 단일형: 이미지 비율 2:1 (800*400), 1:1 (800*800)사용 가능
            - 케로셀형: 이미지 비율 2:1 (800*400)만 사용 가능

        - head: 헤드 정보입니다.

        - profile: 프로필 정보입니다.
            - head와 profile 두 필드를 동시에 노출할 수 없음
            - 케로셀형: 카드별로 head와 profile을 섞어서 사용할 수 없음

        - imageTitle: 이미지를 동반하는 제목 및 설명 정보입니다.
            - 이미지 우측 정렬 고정 (위치 변경 불가)

        - itemListAlignment: itemList 및 itemListAlignment 정렬 정보입니다.
            - "left" 혹은 "right"만 입력 가능

        - itemListSummary: 아이템 가격 정보입니다.
            - itemListSummary 사용 시 itemListAlignment 우측 정렬을 권장

        - title: String, 타이틀 정보입니다.
            - title과 description 합쳐서 글자수 제한
                - 단일형: 최대 200자&12줄
                - 케로셀형: 최대 100자&12줄

        - description: String, 설명 정보입니다.
            - description을 넣는 경우, title이 필수 항목
            - title과 description 합쳐서 글자수 제한
                - 단일형: 최대 200자&12줄
                - 케로셀형: 최대 100자&12줄

        - buttons: Array<Button>, 다양한 액션을 수행할 수 있는 버튼 정보입니다.
            - 단일형: 최대 3개까지 사용 가능
            - 케로셀형: 최대 2개까지 사용 가능

        - buttonLayout: String, 버튼 정렬 정보입니다.
            - "vertical" (세로배치) 혹은 "horizontal" (가로배치) 만 입력 가능
            - 단일형만 buttonLayout 설정 가능, 케로셀형은 가로배치 고정
            - 단일형에서 별도 지정하지 않는 경우 버튼 개수에 따라 배치모양이 결정됨
                - 2개 이하: 가로배치
                - 3개: 세로 배치
            - "horizontal"이면서 버튼이 3개인 경우, 모든 버튼이 미노출됨
    """

    __name__ = "ItemCard"

    itemList: list[ItemList]
    thumbnail: Optional[Thumbnail] = None
    head: Optional[Head] = None
    profile: Optional[Profile] = None
    imageTitle: Optional[ImageTitle] = None
    itemListAlignment: Optional[str] = None
    itemListSummary: Optional[ItemListSummary] = None
    title: Optional[str] = None
    description: Optional[str] = None
    buttons: list[Button] = None
    buttonLayout: Optional[str] = None

    def set_header(self, item: ListItem) -> ItemCard:
        self.header = item
        return self

    def add_button(self, button: Button) -> ItemCard:
        self.buttons.append(button)  # type: ignore
        return self


class OuterItemCard(Struct):
    listCard: ListCard
