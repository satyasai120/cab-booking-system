import math


def distance_km(a, b, c, d):
    return math.sqrt((a - c)**2 + (b - d)**2) * 111


def calculate_price(pickup_lat, pickup_lng, cab_lat, cab_lng, passengers):
    base_fare = 50
    per_km = 12
    surge = 1.2
    pooling_discount = 0.8

    dist = distance_km(pickup_lat, pickup_lng, cab_lat, cab_lng)

    price = (base_fare + dist * per_km) * surge
    price = price * passengers * pooling_discount

    return round(price, 2)