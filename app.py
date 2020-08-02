import requests
import os

# Python Scraping library
from bs4 import BeautifulSoup

# Python Web framework
from flask import Flask, request, abort

# LINE API
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

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

        result = main()

        for r in result["data"]:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    "{}¥n{}¥n{}¥n".format(r["name"], r["addr"], " ".join(r["info"]))
                ),
            )


class KappaController(object):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def get_data(self):
        output = {"data": []}
        result = requests.get(self.url)
        soup = BeautifulSoup(result.content, "html.parser")

        apartment_blocks = soup.find_all("a", class_="imgBox001")
        for apartment_block in apartment_blocks:
            name_block = apartment_block.find("h2")
            info_block = apartment_block.find("section", class_="clear")

            info_list = []
            addr = info_block.find("div").contents[0]
            for info in info_block.find("p", class_="textRight").find_all("span"):
                if "\n" == info.get_text():
                    continue
                else:
                    info_list.append(info.get_text())

            output["data"].append(
                {"name": name_block.contents[-1], "addr": addr, "info": info_list}
            )

        return output


def main():
    print("start kappa!!")
    url = (
        "https://s.shamaison.com/search/list"
        + "?PRF=11&RIL=P119012&SSTA=22048&ESTA=22048&MD=2&CFR=&CTO=&SFR=40&STO=&KD=S10"
    )
    controller = KappaController(url)
    return controller.get_data()


if __name__ == "__main__":
    main()
