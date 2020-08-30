import os
import re

# Python Web framework
from flask import Flask, request, abort

# LINE API
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from src.db.connection import DataBaseConnection
from src.db.models import Receiver


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
    session = DataBaseConnection().session
    receiver = session.query(Receiver).one()

    client_message = event.message.text
    url_fqdn = os.environ["TARGET_URL_FQDN"]
    url_path = receiver.search_url

    if client_message == "検索":
        line_bot_api.reply_message(
            event.reply_token,
            messages=TextSendMessage(url_fqdn + url_path)
        )

    elif client_message == "情報":
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

    elif is_register_url(client_message):
        pattern = "(https://)"
        url = "".join(re.split(pattern, client_message)[-2:])
        receiver.search_url = url.replace(url_fqdn, "")
        session.commit()


def is_register_url(client_message: str):
    pattern = "登録.*https://.*"
    return bool(re.match(pattern, client_message))


if __name__ == "__main__":
    app.run()
