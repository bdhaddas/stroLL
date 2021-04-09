import math
import random
from .JourneyClass import Journey, kilometers, latitude, longitude, coordinates


class RadialJourney(Journey):
    """Creates a journey within a circular region by randomly generating waypoints within a radius"""

    def __init__(self, origin: coordinates, destination: coordinates, radius: kilometers, extraWaypointCount: int, waypoints=None):
        super().__init__(origin, destination, waypoints)
        self.radius = float(radius)
        #print(extraWaypointCount, type(extraWaypointCount), 'eeiuggheiurgherughsearighaseighaerghaeuighaeiughaeiurghaeiru')
        for i in range(extraWaypointCount):
            self.waypoints.append(self.genRandCoordWithinCircle())

    def genRandCoordWithinCircle(self) -> coordinates:
        """Generates a single pair of coordinates within a radius from the origin"""
        origin = self.origin
        radius = self.radius
        R = 6371.0  # Approx. radius of earth
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
