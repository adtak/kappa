import os
import requests

from src.parser import Parser
import src.message_creater as msg


class Controller(object):
    def __init__(self) -> None:
        self.url_fqdn = os.environ["TARGET_URL_FQDN"]
        self.url_path = os.environ["TARGET_URL_PATH"]

    def start(self):
        response = requests.get(self.url_fqdn + self.url_path)
        parser = Parser(self.url_fqdn, response.content)
        result = parser.parse_all()
        return msg.create_message(result["data"])
