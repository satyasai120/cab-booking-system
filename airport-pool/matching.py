import math
from sqlalchemy import select
from models import Cab


def distance(a, b, c, d):
    return math.sqrt((a - c)**2 + (b - d)**2)


async def find_best_cab(session, request):
    result = await session.execute(select(Cab).where(Cab.status == "idle"))
    cabs = result.scalars().all()

    best = None
    best_dist = 999999

    for cab in cabs:
        if cab.available_seats < request.seats_required:
            continue

        d = distance(
            request.pickup_lat,
            request.pickup_lng,
            cab.lat,
            cab.lng
        )

        if d < best_dist:
            best = cab
            best_dist = d

    return best