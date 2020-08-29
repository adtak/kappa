from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import Boolean, DateTime, Float, Integer, String

from src.db.connection import DataBaseConnection

Base = declarative_base()


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    station = Column(String)
    walk_minutes = Column(Integer)
    rooms = relationship("Room", uselist=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())  # noqa E501


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"), nullable=False)
    room_number = Column(String, nullable=False)
    layout = Column(String)
    size = Column(Float)
    rent = Column(Float)
    link_url = Column(String)
    is_vacancy = Column(Boolean, server_default="t")
    is_notify = Column(Boolean, server_default="t")
    apartment = relationship("Apartment")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())  # noqa E501


def main():
    Base.metadata.create_all(DataBaseConnection().engine)


if __name__ == "__main__":
    main()
