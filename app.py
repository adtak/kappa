import os
import requests

# Python Web framework
from flask import Flask, request, abort

# LINE API
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from src.parser import Parser

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

        result = start()

        messages = []
        for r in result["data"]:
            messages.append(
                TextSendMessage(
                    "{}\n{}\n{}\n{}".format(
                        r["name"],
                        r["addr"],
                        r["info"],
                        r["link"]
                    )
                )
            )

        line_bot_api.reply_message(
            event.reply_token,
            messages
        )


def start():
    url_fqdn = "https://s.shamaison.com"
    url_path = "/search/list" \
               "?PRF=11&RIL=P119012&SSTA=22048&ESTA=22048&MD=2&CFR=&CTO=&SFR=40&STO=&KD=S10"

    result = requests.get(url_fqdn + url_path)
    parser = Parser(url_fqdn, result.content)

    return parser.parse_all()


if __name__ == "__main__":
    app.run()
