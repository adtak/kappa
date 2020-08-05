import os

# LINE API
from linebot import LineBotApi
from linebot.models import TextSendMessage

from src.controller import Controller

channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
user_id = os.environ["LINE_PUSH_RECEIVER_ID"]
line_bot_api = LineBotApi(channel_access_token)


def main():
    messages = Controller().start()

    line_bot_api.push_message(
        user_id,
        messages=[TextSendMessage(m) for m in messages]
    )


if __name__ == "__main__":
    main()
