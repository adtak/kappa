import os

# LINE API
from linebot import LineBotApi
from linebot.models import TextSendMessage

from src.controller import Controller

channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(channel_access_token)


def main():
    controller = Controller()

    controller.start()

    result = controller.result

    if len(result) > 0:
        messages = ["本日の新着物件をお知らせするよ！"] + result
    else:
        messages = ["本日の新着物件はないよ！"]

    user_id = controller.get_user_id()
    for m in messages:
        line_bot_api.push_message(
            user_id,
            messages=TextSendMessage(m)
        )

    controller.final()


if __name__ == "__main__":
    main()
