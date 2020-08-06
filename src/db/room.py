from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import DateTime, Float, Integer, String


Base = declarative_base()


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id", nullable=False))
    room_number = Column(String, nullable=False)
    layout = Column(String)
    size = Column(String)
    rent = Column(Float)
    apartment = relationship("Apartment")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())  # noqa E501
