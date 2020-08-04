import requests
# Python Scraping library
from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self, url_fqdn: str, html: str) -> None:
        self._url_fqdn = url_fqdn
        self._soup = BeautifulSoup(html, "html.parser")

    def parse_all(self):
        res = {"data": []}
        for elem in self._soup.find_all("a", class_="imgBox001"):
            res["data"].append(
                {
                    "name": self.parse_name(elem),
                    "addr": self.parse_addr(elem),
                    "info": self.parse_info(elem),
                    "link": self._url_fqdn + self.parse_link(elem),
                }
            )
        return res

    def parse_name(self, html):
        return html.find("h2").contents[-1]

    def parse_addr(self, html):
        return html.find("section", class_="clear").find("div").contents[0]

    def parse_info(self, html):
        info_list = []
        for span_tag in html.find("section", class_="clear") \
                            .find("p", class_="textRight").find_all("span"):

            if "\n" == span_tag.get_text():
                continue
            else:
                info_list.append(span_tag.get_text())
        return " ".join(info_list)

    def parse_link(self, html):
        return html.get_attribute_list("href")[0]


if __name__ == "__main__":
    url_fqdn = "https://s.shamaison.com"
    url_path = "/search/list"
    + "?PRF=11&RIL=P119012&SSTA=22048&ESTA=22048&MD=2&CFR=&CTO=&SFR=40&STO=&KD=S10"

    result = requests.get(url_fqdn + url_path)
    parser = Parser(url_fqdn, result.content)
    print(parser.parse_all())
