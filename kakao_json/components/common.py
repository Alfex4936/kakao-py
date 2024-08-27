from __future__ import annotations

from typing import Any, Mapping, Optional

from msgspec import Struct

__all__ = [
    "Button",
    "ContextControl",
    "CarouselHeader",
    "Link",
    "Profile",
    "Social",
    "Thumbnail",
    "ListItem",
]


class Profile(Struct, omit_defaults=True):
    """# Profile

    카드의 프로필 정보입니다.

    이미지 사이즈는 180px X 180px 추천합니다.

    # ! 현재 미지원 API

    # ItemCard는 다른 profile 값을 갖음

    ## Attributes:
        - nickname: String, 프로필 이름 (필수)

        - imageUrl: String, 프로필 이미지

        --- 아래는 ItemCard 용

        - title: String, 프로필 타이틀 정보입니다. (필수)
            - 최대 15글자

        - imageUrl: String, 프로필 이미지 정보입니다. URL 형식

        - width: int, 프로필 이미지의 넓이 정보입니다.
            - 1:1 비율에 맞게 입력 필요
            - 실제 이미지 사이즈와 다른 값일 경우 원본 이미지와 다르게 표현될 수 있음

        - height: int, 	프로필 이미지의 높이 정보입니다.
    """

    nickname: Optional[str] = None
    imageUrl: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    title: Optional[str] = None

    def for_item_card(
        self,
        title: str,
        url: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> Profile:
        self.title = title
        self.url = url
        self.width = width
        self.height = height

        return self


class Social(Struct):
    """# Social

    카드의 소셜 정보입니다.

    # ! 현재 미지원 API

    ## Attributes:
        - like: int,

        - comment: int,

        - share: int,
    """

    ...


class Link(Struct, omit_defaults=True):
    """# Link

    Information. 링크 우선순위 링크는 다음과 같은 우선순위를 갖습니다.

    pc: pc < web
    모바일: mobile < web

    예를 들면, pc에 대하여 링크 값이 webURL, pcURL를 가지면 위 규칙에 따라 webURL이 노출됩니다.
    모바일 기기에 대하여 Link의 값이 webURL, mobileURL를 가지면 위 규칙에 따라 webURL이 노출됩니다.

    ## Attributes:
        - pc: String, pc의 웹을 실행하는 link입니다.

        - mobile: String, mobile의 웹을 실행하는 link입니다.

        - web: String, 모든 기기에서 웹을 실행하는 link입니다.
    """

    pc: Optional[str] = None
    mobile: Optional[str] = None
    web: Optional[str] = None


class Thumbnail(Struct, omit_defaults=True):
    """# Thumbnail

    ## With ItemCard

    단일형: 이미지 비율 2:1 (800*400), 1:1 (800*800)사용 가능

    케로셀형: 이미지 비율 2:1 (800*400)만 사용 가능

    ## Attributes:
        - imageUrl: String, 이미지의 url입니다.

        - link: String, 이미지 클릭시 작동하는 link입니다.

        - fixedRatio: boolean, 기본값: false
                - `true`: 이미지 영역을 1:1 비율로 두고 이미지의 원본 비율을 유지합니다. 이미지가 없는 영역은 흰색으로 노출합니다.
                - `false`: 이미지 영역을 2:1 비율로 두고 이미지의 가운데를 크롭하여 노출합니다.
                - ※ 케로셀 내에서는 모든 이미지가 정사각형 (1:1) 혹은 모든 이미지가 와이드형 (2:1)으로 통일되어야 합니다.

        - width: int, `fixedRatio를 true`로 설정할 경우 필요한 값입니다. 실제 이미지 사이즈와 다른 값일 경우 원본이미지와 다르게 표현될 수 있습니다.

        - height: int, `fixedRatio를 true`로 설정할 경우 필요한 값입니다. 실제 이미지 사이즈와 다른 값일 경우 원본이미지와 다르게 표현될 수 있습니다.
    """

    imageUrl: str
    link: Optional[Link] = None
    fixedRatio: Optional[bool] = None
    width: Optional[int] = None
    height: Optional[int] = None

    def set_image(self, url: str) -> Thumbnail:
        self.imageUrl = url
        return self

    def for_list_card(self, url: str, width: int, height: int) -> Thumbnail:
        self.imageUrl = url
        self.width = width
        self.height = height
        return self


class ListItem(Struct, omit_defaults=True):
    title: str
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    link: Optional[Link] = None
    action: Optional[str] = None
    blockId: Optional[str] = None
    messageText: Optional[str] = None
    extra: Optional[Mapping[str, Any]] = None

    def set_action(self, action: str) -> ListItem:
        if action not in ["message", "block"]:
            raise Exception("unknown action for Button")
        self.action = action
        return self

    def set_action_block(self) -> ListItem:
        self.action = "block"
        return self

    def set_action_message(self) -> ListItem:
        self.action = "message"
        return self

    def set_title(self, title: str) -> ListItem:
        if not self.action:
            self.action = "message"
        self.title = title
        return self

    def set_desc(self, desc: str) -> ListItem:
        if not self.action:
            self.action = "message"
        self.description = desc
        return self

    def set_image(self, url: str) -> ListItem:
        self.imageUrl = url
        return self

    def set_msg(self, messageText: str) -> ListItem:
        if not self.action:
            self.action = "message"
        """사용자의 발화로 messageText를 내보냅니다. (바로가기 응답의 메세지 연결 기능과 동일)"""
        self.messageText = messageText
        return self

    def set_link(self, url: str) -> ListItem:
        """web > pc == mobile"""
        if self.link is None:
            self.link = Link(web=url, pc=None, mobile=None)
        else:
            self.link.web = url
        return self

    def set_link_pc(self, url: str) -> ListItem:
        """web > pc == mobile"""
        if self.link is None:
            self.link = Link(pc=url, web=None, mobile=None)
        else:
            self.link.pc = url
        return self

    def set_link_mobile(self, url: str) -> ListItem:
        """web > pc == mobile"""
        if self.link is None:
            self.link = Link(mobile=url, pc=None, web=None)
        else:
            self.link.mobile = url
        return self


class Button(Struct, omit_defaults=True):
    """# Button

    ## action 종류

    - webLink: 웹 브라우저를 열고 webLinkUrl 의 주소로 이동합니다.
    - message: 사용자의 발화로 messageText를 실행합니다. (바로가기 응답의 메세지 연결 기능과 동일)
    - phone: phoneNumber에 있는 번호로 전화를 겁니다.
    - block: blockId를 갖는 블록을 호출합니다. (바로가기 응답의 블록 연결 기능과 동일)
    - messageText가 있다면, 해당 messageText가 사용자의 발화로 나가게 됩니다.
    - messageText가 없다면, button의 label이 사용자의 발화로 나가게 됩니다.
    - share: 말풍선을 다른 유저에게 공유합니다. share action은 특히 케로셀을 공유해야 하는 경우 유용합니다.
    - operator (베타): 상담직원 연결 기능을 제공합니다.
        - 링크: [상담직원 연결](https://i.kakao.com/docs/key-concepts-plugin#%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0-%EC%84%A4%EC%A0%95-%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8)

    ## Attributes:
        - label: String, 버튼에 적히는 `text`입니다. 버튼 14자(가로배열 2개 8자)

        - action: String, 버튼 클릭시 수행될 작업입니다.
                - webLink, message, phone, block, share, operator

        - webLinkUrl: String, 웹 브라우저를 열고 `webLinkUrl` 의 주소로 이동합니다. (URL)

        - messageText: String,

                - `message`: 사용자의 발화로 messageText를 내보냅니다. (바로가기 응답의 메세지 연결 기능과 동일)
                - `block`: 블록 연결시 사용자의 발화로 노출됩니다.

        - phoneNumber: String, `phoneNumber`에 있는 번호로 전화를 겁니다.

        - blockId: String, `blockId`를 갖는 블록을 호출합니다. (바로가기 응답의 블록 연결 기능과 동일)

        - extra: Map[String, Any], `block`이나 `message` action으로 블록 호출시, 스킬 서버에 추가적으로 제공하는 정보
    """

    label: str = ""
    action: str = ""
    webLinkUrl: Optional[str] = None
    messageText: Optional[str] = None
    phoneNumber: Optional[str] = None
    blockId: Optional[str] = None
    extra: Optional[Mapping[str, Any]] = None

    def set_label(self, label: str) -> Button:
        self.label = label
        return self

    def set_link(self, link: str) -> Button:
        if not self.action:
            self.action = "webLink"
        self.webLinkUrl = link
        return self

    def set_msg(self, msg: str) -> Button:
        if not self.action:
            self.action = "message"
        self.messageText = msg
        return self

    def set_number(self, number: str) -> Button:
        if not self.action:
            self.action = "phone"
        self.phoneNumber = number
        return self

    def set_action(self, action: str) -> Button:
        if action not in ["webLink", "message", "phone", "block", "share", "operator"]:
            raise Exception("unknown action for Button")
        self.action = action

        return self

    def set_action_web(self) -> Button:
        self.action = "webLink"
        self.webLinkUrl = "http://CHANGE.ME"
        return self

    def set_action_msg(self) -> Button:
        self.action = "message"
        # if not self.messageText:
        #     self.messageText = self.label if self.label else ""
        return self

    def set_action_call(self) -> Button:
        self.action = "phone"
        self.phoneNumber = "010-CHANGE-ME"
        return self

    def set_action_block(self) -> Button:
        self.action = "block"
        self.blockId = "id-change-me"
        return self

    def set_action_share(self) -> Button:
        self.action = "share"
        return self

    def set_action_operator(self) -> Button:
        self.action = "operator"
        return self

    def set_thumbnail(self, thumbnail: Thumbnail) -> Button:
        self.thumbnail = thumbnail
        return self


"""
"carousel": {
    "type": "commerceCard",
    "header": {
        "title": "커머스 카드\n케로셀 헤드 예제",
        "thumbnail": {
            "imageUrl": "https://t1.kakaocdn.net/openbuilder/sample/lj3JUcmrzC53YIjNDkqbWK.jpg"
        }
    },
}
"""


class CarouselHeader(Struct):
    """# CarouselHeader

    ## Attributes:
        - title: String, 케로셀 헤드 제목
            - 최대 2줄 (한 줄에 들어갈 수 있는 글자 수는 기기에 따라 달라집니다.)

        - description: String, 케로셀 헤드 설명
            - 최대 3줄 (한 줄에 들어갈 수 있는 글자 수는 기기에 따라 달라집니다.)

        - thumbnail: String, 케로셀 헤드 배경 이미지
            - 현재 imageUrl 값만 지원합니다.
    """

    title: str
    description: str
    thumbnail: Thumbnail


class ContextValue(Struct):
    """# ContextValue

    context control 필드는 블록에서 생성한 outputContext의 lifeSpan, params 등을 제어할 수 있습니다.

    ## Attributes:
        - name: String, 수정하려는 output 컨텍스트의 이름

        - lifeSpan: int, 수정하려는 ouptut 컨텍스트의 lifeSpan

        - params: Map<String, String>, output 컨텍스트에 저장하는 추가 데이터

    ## Example

    - abc output 컨텍스트의 lifeSpan을 10, ttl을 60로, params의 key1에 val1, key2에 val2를 추가합니다.
    - def name을 갖는 ContextValue의 param처럼, 다른 타입들 또한 stringify 하여 저장할 수 있습니다.
    - ghi name을 갖는 ContextValue처럼, lifeSpan을 0으로 바꿔서 삭제할 수 있습니다.

    ```json
    {
        "version": "2.0",
        "context": {
            "values": [
            {
                "name": "abc",
                "lifeSpan": 10,
                "params": {
                "key1": "val1",
                "key2": "val2"
                }
            },
            {
                "name": "def",
                "lifeSpan": 5,
                "params": {
                "key3": "1",
                "key4": "true",
                "key5": "{\"jsonKey\": \"jsonVal\"}"
                }
            },
            {
                "name": "ghi",
                "lifeSpan": 0
            }
            ]
        }
    }
    ```
    """

    name: str
    lifeSpan: int
    params: Optional[Mapping[str, str]]


class ContextControl(Struct):
    """# ContextControl

    context control 필드는 블록에서 생성한 outputContext의 lifeSpan, params 등을 제어할 수 있습니다.

    ## Attributes:
        - values: ContextValue

    """

    values: list[ContextValue]
