from src.db.models import Apartment, Room


def create_message(room: Room):
    apartment: Apartment = room.apartment
    return "{}\n{}\n{}\n{}".format(
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
