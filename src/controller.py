import os
import re
import requests
from typing import List

from src.db.connection import DataBaseConnection
from src.db.models import Apartment, Room, Receiver
from src.parser import ParseResult, Parser
import src.message_creater as msg


class Controller(object):
    def __init__(self) -> None:
        self.session = DataBaseConnection().session
        self.receiver = self.session.query(Receiver).one()
        self.url_fqdn = os.environ["TARGET_URL_FQDN"]
        self.url_path = self.receiver.search_url
        self.result = None

    def start(self):
        data: List[ParseResult] = self.scraping()
        self.update_data(data)
        data = self.select_notification()
        self.result = msg.create_message(data)

    def final(self):
        room = self.session.query(Room).filter(Room.is_notify.is_(True))
        for r in room:
            r.is_notify = False
        self.session.commit()

    def scraping(self) -> List[ParseResult]:
        response = requests.get(self.url_fqdn + self.url_path)

        parser = Parser(self.url_fqdn, response.content)
        result = parser.parse_all()

        return result

    def update_data(self, data: List[ParseResult]):
        vacancy_room_ids = []
        for d in data:
            # insert new apartment
            apartment = self.session.query(Apartment).filter(
                Apartment.name == d.name,
                Apartment.address == d.address).one_or_none()
            if apartment:
                pass
            else:
                apartment = Apartment()
                apartment.name = d.name
                apartment.address = d.address
                apartment.station = d.station
                apartment.walk_minutes = re.search("\d+", d.walk_minutes).group()  # noqa W605
                self.session.add(apartment)

            # upsert room
            room = self.session.query(Room).filter(
                Room.apartment_id == apartment.id,
                Room.room_number == d.room_number
            ).one_or_none()
            room = room if room else Room()

            before_is_vacancy = room.is_vacancy

            room.apartment_id = apartment.id
            room.room_number = d.room_number
            room.layout = d.layout
            room.size = re.search("\d+[.]\d+", d.size).group()  # noqa W605
            room.rent = re.search("\d+[.]\d+", d.rent).group()  # noqa W605
            room.link_url = d.link_url
            room.is_vacancy = True
            room.is_notify = True if (room.id is None) or (before_is_vacancy is False) \
                else room.is_notify

            self.session.add(room)

            vacancy_room_ids.append(room.id)

        self.session.commit()

        no_vacancy_room = self.session.query(Room). \
            filter(Room.is_vacancy.is_(True)). \
            filter(Room.id.notin_(vacancy_room_ids)).all()
        for r in no_vacancy_room:
            r.is_vacancy = False
            # r.is_notify = True
        self.session.commit()

    def select_notification(self):
        return self.session.query(Room).filter(Room.is_notify.is_(True)).all()

    def get_user_id(self):
        return self.receiver.user_id


if __name__ == "__main__":
    Controller().start()
