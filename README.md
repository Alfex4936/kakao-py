<div align="center">
<p>
    <img width="680" src="https://raw.githubusercontent.com/Alfex4936/kakaoChatbot-Ajou/main/imgs/chatbot.png">
</p>

<h2>카카오톡 챗봇 빌더 도우미</h2>
<h3>Python언어 전용</h3>
</div>

# 소개

Python 언어로 카카오 챗봇 서버를 만들 때 좀 더 쉽게 JSON 메시지 응답을 만들 수 있게 도와줍니다.

SimpleText, SimpleImage, ListCard, Carousel, BasicCard, CommerceCard, ItemCard 등의

챗봇 JSON 데이터를 쉽게 만들 수 있도록 도와줍니다.

# 설치
```bash
pip install pykakao
```


# 사용법

## ListCard 예제

```json
/*
Result: {
  "template": {
    "outputs": [
      {
        "listCard": {
          "buttons": [
            {
              "label": "그냥 텍스트 버튼",
              "action": "message"
            },
            {
              "label": "link label",
              "action": "webLink",
              "webLinkUrl": "https://google.com"
            },
            {
              "label": "share label",
              "action": "share",
              "messageText": "카톡에 보이는 메시지"
            },
            {
              "label": "call label",
              "action": "phone",
              "phoneNumber": "010-1234-5678"
            }
          ],
          "header": {
            "title": "리스트 카드 제목!"
          },
          "items": [
            {
              "title": "title",
              "description": "description",
              "link": {
                "web": "https://naver.com"
              }
            }
          ]
        }
      }
    ],
    "quickReplies": [
      {
        "action": "message",
        "label": "오늘",
        "messageText": "오늘 공지 보여줘"
      },
      {
        "action": "message",
        "label": "어제",
        "messageText": "어제 공지 보여줘"
      }
    ]
  },
  "version": "2.0"
}
*/
```

## Usage
```python
from pykakao.kakao import Kakao

k = Kakao()

basic_card = k.init_basic_card()
basic_card.set_title("title").set_desc("hello").add_button(
    k.init_button("labell").set_action_web().set_link("https://naver.com")
)

k.add_output(basic_card)

msgspec.json.encode(k)
```
