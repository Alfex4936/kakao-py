from dataclasses import dataclass
from typing import Dict, Union

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from kakao_json import Button, Kakao, ListItem

app = FastAPI(title="FastAPI kakao-py example", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/list_card")
def read_item(req: Dict):
    @dataclass
    class Item:
        name: str
        number: int

    # Make your python objects
    items = [Item(f"I {i}", i + 2) for i in range(5)]
    append = items.append

    # kakao-json part
    k = Kakao()
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

    carousel = k.init_carousel()
    for i in range(5):
        basic_card = k.init_basic_card()
        basic_card.set_title(f"Hey {i}").set_image("https://kakao")
        carousel.add_card(basic_card)

    k.add_output(list_card)
    k.add_output(carousel)

    # import json

    # print(json.loads(k.to_json()))

    return k.to_json()


if __name__ == "__main__":
    uvicorn.run(app)
