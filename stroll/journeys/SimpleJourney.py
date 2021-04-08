import math
import random
from .JourneyClass import Journey, kilometers, latitude, longitude, coordinates


class SimpleJourney(Journey):
    """Creates a simple journey from origin to destination with waypoints to visit along the way"""

    def __init__(self, origin: coordinates, destination: coordinates, waypoints=[]):
        super().__init__(origin, destination, waypoints)
