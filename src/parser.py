# Python Scraping library
from bs4 import BeautifulSoup
import re
from typing import NamedTuple


class ParseResult(NamedTuple):
    name: str
    address: str
    station: str
    walk_minutes: str
    room_number: str
    layout: str
    size: str
    rent: str
    link_url: str


class Parser(object):
    def __init__(self, url_fqdn: str, html: str) -> None:
        self._url_fqdn = url_fqdn
        self._soup = BeautifulSoup(html, "html.parser")

    def parse_all(self):
        res = []
        for elem in self._soup.find_all("a", class_="imgBox001"):
            name, room_number = self.parse_name(elem)
            address = self.parse_address(elem)
            station, walk_minutes, layout, size, rent = self.parse_info(elem)
            link_url = self.parse_link(elem)

            res.append(
                ParseResult(
                    name, address, station, walk_minutes,
                    room_number, layout, size, rent, self._url_fqdn+link_url
                )
            )
        return res

    def parse_name(self, html):
        name = html.find("h2").contents[-1]
        split_name = re.split("(\d+)", name)  # noqa W605
        return split_name[0], "".join(split_name[1:])

    def parse_address(self, html):
        return html.find("section", class_="clear").find("div").contents[0]

    def parse_info(self, html):
        info_list = []
        for span_tag in html.find("section", class_="clear") \
                            .find("p", class_="textRight").find_all("span"):

            if "\n" == span_tag.get_text():
                continue
            else:
                text = span_tag.get_text()
                texts = [text] if u"\xa0" not in text else text.split(u"\xa0")
                info_list += texts
        return info_list

    def parse_link(self, html):
        return html.get_attribute_list("href")[0]
