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

    results = controller.results

    for receiver, messages in results.items():
        if len(messages) > 0:
            messages = ["本日の新着物件をお知らせするよ！"] + messages
        else:
            messages = ["本日の新着物件はないよ！"]

        for m in messages:
            line_bot_api.push_message(
                receiver,
                messages=TextSendMessage(m)
            )


if __name__ == "__main__":
    main()
