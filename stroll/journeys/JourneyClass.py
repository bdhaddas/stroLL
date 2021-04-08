import googlemaps
import json
import math
import random
from abc import ABC, abstractmethod

# with open('apikey.txt') as f:
#     api_key = f.readline()
#     f.close
gmaps = googlemaps.Client(key='AIzaSyCzSDLwakvV-7nq3GXYc1sAapKFiAL8Fd4')


# type definitions
kilometers, latitude, longitude = float, float, float
# type alias (Should work with latest Python)
coordinates = [latitude, longitude]


def distanceBetweenCoords(lat1: latitude, lon1: longitude, lat2: latitude, lon2: longitude) -> kilometers:
    R = 6378.137
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * \
        math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d


class Journey(ABC):  # * Abstract Class
    @abstractmethod
    def __init__(self, origin: coordinates, destination: coordinates, waypoints=[]):
        self.origin = origin
        self.destination = destination
        self.waypoints = waypoints
    
    @abstractmethod
    def getGmapsDirections(self, mode="walking") -> str:
        directions = gmaps.directions(
            self.origin, self.destination, waypoints=self.waypoints, mode=mode
        )
        # with open("directions.json", "w+") as json_file:
        #    json.dump(directions, json_file, indent = 4, sort_keys=True)
        return directions

    @abstractmethod
    def makeVisitAttractions(self, attractions: [coordinates], maxConnectDistance: kilometers = 3):
        """Updates waypoints along a journey to visit nearby attractions where each attraction has to be within maxConnectDistance of a waypoint"""
        waypoints = self.waypoints
        newWaypoints = []
        usedUpAttractions = set()

        for coordWaypoint in waypoints:
            newWaypoints.append(coordWaypoint)

            latWaypoint, lngWaypoint = coordWaypoint[0], coordWaypoint[1]
            closestAttraction, closestDistance = None, maxConnectDistance

            # find closest attraction that hasn't already been added to the new path
            for coordAttraction in attractions:
                latAttraction, lngAttraction = coordAttraction[0], coordAttraction[1]
                distance = distanceBetweenCoords(
                    latWaypoint, lngWaypoint, latAttraction, lngAttraction)
                if not (str(coordAttraction.copy()) in usedUpAttractions) and (distance < closestDistance):
                    closestAttraction, closestDistance = coordAttraction, distance

            # add the closest attraction as next in the path
            if closestAttraction:
                usedUpAttractions.add(str(closestAttraction.copy()))
                newWaypoints.append(closestAttraction)

        self.waypoints = newWaypoints
