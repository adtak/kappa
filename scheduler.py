import os

# LINE API
from linebot import LineBotApi
from linebot.models import TextSendMessage

channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
channel_secret = os.environ["LINE_CHANNEL_SECRET"]
user_id = os.environ["LINE_PUSH_RECEIVER_ID"]
line_bot_api = LineBotApi(channel_access_token)


def main():
    pushText = TextSendMessage(text="test")
    line_bot_api.push_message(user_id, messages=pushText)


if __name__ == "__main__":
    main()
