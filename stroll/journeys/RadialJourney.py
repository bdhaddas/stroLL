import googlemaps
import math
import random
from .JourneyClass import Journey, kilometers, latitude, longitude, coordinates


def genRandCoordWithinCircle(origin: coordinates, radius: kilometers) -> coordinates:
    """Generates a single pair of coordinates within a radius from the origin"""
    R = 6371  # Approx. radius of earth
    pi = math.pi
    Lat, Lng = (origin[0] * pi) / 180, (origin[1] * pi) / 180
    d = radius * math.sqrt(random.random()) / R
    i = random.uniform(0, 360)
    brng = i * pi / 180
    pLat = (math.asin(math.sin(Lat) * math.cos(d) + math.cos(Lat)
            * math.sin(d) * math.cos(brng))) * 180 / pi
    pLng = ((Lng + math.atan2(math.sin(brng) * math.sin(d) * math.cos(Lat),
            math.cos(d) - math.sin(Lat) * math.sin(pLat))) * 180) / pi
    return [pLat, pLng]


class RadialJourney(Journey):
    """Generates waypoints within a defined circular region"""
    def __init__(origin: coordinates, radius: kilometers, waypointCount: int) -> list[coordinates]:
        waypoints = []

        for _ in range(waypointCount):
            waypoints.append(genRandCoordWithinCircle(origin, radius))

        return waypoints
