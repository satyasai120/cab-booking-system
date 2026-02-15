from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Server running"}


from database import engine

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        print("DB connected")

from models import Base

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Passenger

SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@app.post("/passenger")
async def create_passenger(name: str):
    async with SessionLocal() as session:
        p = Passenger(name=name)
        session.add(p)
        await session.commit()
    return {"msg": "created"}


from fastapi import FastAPI
from database import engine
from models import Base

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
def home():
    return {"status": "running"}

from database import SessionLocal
from models import Cab


@app.post("/cab")
async def create_cab(
    seats: int,
    luggage: int,
    lat: float,
    lng: float
):
    async with SessionLocal() as session:
        cab = Cab(
            total_seats=seats,
            available_seats=seats,
            luggage_capacity=luggage,
            lat=lat,
            lng=lng,
            status="idle"
        )

        session.add(cab)
        await session.commit()

    return {"message": "Cab added"}

from models import RideRequest
from matching import find_best_cab


@app.post("/ride")
async def request_ride(
    lat: float,
    lng: float,
    seats: int
):
    async with SessionLocal() as session:

        # create request
        req = RideRequest(
            pickup_lat=lat,
            pickup_lng=lng,
            seats_required=seats
        )
        session.add(req)
        await session.commit()
        await session.refresh(req)

        # find cab
        cab = await find_best_cab(session, req)

        if not cab:
            return {"message": "No cab available"}

        # assign cab
        cab.available_seats -= seats
        cab.status = "busy"

        req.status = "assigned"
        req.cab_id = cab.id

        await session.commit()

        return {
            "ride_id": req.id,
            "cab_id": cab.id,
            "message": "Cab assigned"
        }
    
from models import Ride
from pricing import calculate_price

from sqlalchemy import select
from models import Ride, Cab


@app.post("/ride/complete/{ride_id}")
async def complete_ride(ride_id: int):
    async with SessionLocal() as session:

        result = await session.execute(
            select(Ride).where(Ride.id == ride_id)
        )
        ride = result.scalar_one_or_none()

        if not ride:
            return {"message": "Ride not found"}

        if ride.status == "completed":
            return {"message": "Already completed"}

        result = await session.execute(
            select(Cab).where(Cab.id == ride.cab_id)
        )
        cab = result.scalar_one()

        # 🔥 restore seats
        cab.available_seats += ride.seats_booked

        # if fully free → idle
        if cab.available_seats == cab.total_seats:
            cab.status = "idle"

        ride.status = "completed"

        await session.commit()

        return {"message": "Ride completed, cab available again"}