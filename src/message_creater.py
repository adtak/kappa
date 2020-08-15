from typing import List

from src.db.models import Apartment, Room


def create_message(rooms: List[Room]):
    messages = []
    for room in rooms:
        apartment: Apartment = room.apartment
        messages.append(
            "{}\n{}\n{}\n{}".format(
                apartment.name,
                apartment.address,
                "{} 徒歩{}分 {} {}㎡ {}万円".format(
                    apartment.station,
                    apartment.walk_minutes,
                    room.layout,
                    room.size,
                    room.rent),
                room.link_url
            )
        )
    return messages
