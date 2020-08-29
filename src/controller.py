import os
import re
import requests
from typing import Dict, List, NamedTuple

from src.db.connection import DataBaseConnection
from src.db.models import Apartment, Room, Receiver, Notification
from src.parser import ParseResult, Parser
import src.message_creater as msg


class ReceiverInfo(NamedTuple):
    receiver_id: str
    search_url: str


class NotificationInfo(NamedTuple):
    receiver: str
    messages: List[str]


class Controller(object):
    def __init__(self) -> None:
        self.url_fqdn = os.environ["TARGET_URL_FQDN"]
        self.session = DataBaseConnection().session

        self.receivers: List[ReceiverInfo] = self.get_receivers()
        self.vacancy_room_ids: List[int] = []
        self.results: Dict[str, List[str]] = dict()

    def get_receivers(self):
        receivers = self.session.query(Receiver).all()
        return [ReceiverInfo(r.id, r.search_url) for r in receivers]

    def start(self):
        self.initial()
        self.main()
        self.final()

    def initial(self):
        self.session.query(Notification).delete()

    def main(self):
        for r in self.receivers:
            data: List[ParseResult] = self.scraping(r.search_url)
            self.update_data(r.receiver_id, data)

        notifications = self.select_notification()
        for n in notifications:
            receiver = n.receiver.receiver
            message = msg.create_message(n.room)
            messages = self.results.get(receiver, [])
            messages.append(message)
            self.results[receiver] = messages

    def final(self):
        no_vacancy_room = self.session.query(Room). \
            filter(Room.is_vacancy.is_(True)). \
            filter(Room.id.notin_(self.vacancy_room_ids)).all()
        for r in no_vacancy_room:
            r.is_vacancy = False
            # r.is_notify = True
        self.session.commit()

        room = self.session.query(Room).filter(Room.is_notify.is_(True))
        for r in room:
            r.is_notify = False
        self.session.commit()

    def scraping(self, url_path: str) -> List[ParseResult]:
        response = requests.get(self.url_fqdn + url_path)

        parser = Parser(self.url_fqdn, response.content)
        result = parser.parse_all()

        return result

    def update_data(self, receiver_id: str, data: List[ParseResult]):
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
            room = room or Room()

            if room.is_notify is True:
                pass
            else:
                room.apartment_id = apartment.id
                room.room_number = d.room_number
                room.layout = d.layout
                room.size = re.search("\d+[.]\d+", d.size).group()  # noqa W605
                room.rent = re.search("\d+[.]\d+", d.rent).group()  # noqa W605
                room.link_url = d.link_url
                room.is_vacancy_before = room.is_vacancy
                room.is_vacancy = True
                room.is_notify = True if (room.id is None) or (room.is_vacancy_before is False) \
                    else room.is_notify

                self.session.add(room)

                self.vacancy_room_ids.append(room.id)

            # insert notification
            notification = Notification()
            notification.receiver_id = receiver_id
            notification.room_id = room.id

            self.session.add(notification)

        self.session.commit()

    def select_notification(self) -> List[Notification]:
        return self.session.query(Notification).all()


if __name__ == "__main__":
    Controller().start()
