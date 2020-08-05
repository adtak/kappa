import os
import requests

# LINE API
from linebot import LineBotApi
from linebot.models import TextSendMessage

from src.parser import Parser
import src.message_creater as msg

channel_access_token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
user_id = os.environ["LINE_PUSH_RECEIVER_ID"]
line_bot_api = LineBotApi(channel_access_token)


def main():
    result = start()

    line_bot_api.push_message(
        user_id,
        messages=[TextSendMessage(m) for m in msg.create_message(result["data"])])


def start():
    url_fqdn = "https://s.shamaison.com"
    url_path = "/search/list" \
               "?PRF=11&RIL=P119012&SSTA=22048&ESTA=22048&MD=2&CFR=&CTO=&SFR=40&STO=&KD=S10"

    result = requests.get(url_fqdn + url_path)
    parser = Parser(url_fqdn, result.content)

    return parser.parse_all()


if __name__ == "__main__":
    main()
