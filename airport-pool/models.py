from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True)
    name = Column(String)

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True)
    name = Column(String)


from sqlalchemy import Column, Integer, Float, String
from database import engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cab(Base):
    __tablename__ = "cabs"

    id = Column(Integer, primary_key=True, index=True)
    total_seats = Column(Integer)
    available_seats = Column(Integer)
    luggage_capacity = Column(Integer)
    lat = Column(Float)
    lng = Column(Float)
    status = Column(String, default="idle")


from sqlalchemy import ForeignKey


class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True)
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    seats_required = Column(Integer)
    status = Column(String, default="waiting")
    cab_id = Column(Integer, ForeignKey("cabs.id"), nullable=True)

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True)
    cab_id = Column(Integer)
    request_id = Column(Integer)
    total_price = Column(Float)

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True)
    cab_id = Column(Integer)
    request_id = Column(Integer)
    total_price = Column(Float)
    seats_booked = Column(Integer)
    status = Column(String, default="ongoing")