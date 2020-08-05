import os

# Python Web framework
from flask import Flask, request, abort

# LINE API
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from src.controller import Controller


# make instance
app = Flask(__name__)

channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
channel_secret = os.environ["LINE_CHANNEL_SECRET"]
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


# route for checking deploy
@app.route("/")
def hello_world():
    return "hello world!"


# POST from LINE
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    client_message = event.message.text
    if client_message == "検索":

        messages = Controller().start()

        line_bot_api.reply_message(
            event.reply_token,
            messages=[TextSendMessage(m) for m in messages]
        )

    elif client_message == "show properties":
        _type = event.source.type
        msg = f"TYPE : {_type}\n"

        if _type == 'user':
            msg += f"USER ID : {event.source.user_id}"

        elif _type == 'group':
            msg += f"GROUP ID : {event.source.group_id}\n"
            msg += f"USER ID : {event.source.user_id}"

        elif _type == 'room':
            msg += f"ROOM ID : {event.source.room_id}\n"
            msg += f"USER ID : {event.source.user_id}"

        else:
            msg += "UNKNOWN TYPE"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
        )


if __name__ == "__main__":
    app.run()
