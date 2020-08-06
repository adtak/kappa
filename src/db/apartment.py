from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import DateTime, Integer, String


Base = declarative_base()


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    station = Column(String)
    walk_time = Column(Integer)
    rooms = relationship("Room", uselist=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())  # noqa E501
