import googlemaps
import json
import math
import random

# with open('apikey.txt') as f:
#     api_key = f.readline()
#     f.close
gmaps = googlemaps.Client(key='')


# type definitions
kilometers, latitude, longitude = float, float, float
coordinates = list[latitude, longitude]  # type alias (Should work in VSCode)


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


def genWaypointsWithinCircle(origin: coordinates, radius: kilometers, waypointCount: int) -> list[coordinates]:
    waypoints = []

    for _ in range(waypointCount):
        waypoints.append(genRandCoordWithinCircle(origin, radius))

    # gmaps.directions(origin, destination, waypoints=waypoints, mode="walking")
    return waypoints


#! Deprecated
def coord_radial(origin, radius, compassDirection):  # ? generateRadialPath(origin
    radius_deg = radius / 111.32
    half_radius_deg = radius_deg / 2
    coord_points = []
    offset_angle = 0
    if compassDirection == "North":
        offset_angle = 0
    elif compassDirection == "East":
        offset_angle = 90
    elif compassDirection == "South":
        offset_angle = 180
    elif compassDirection == "West":
        offset_angle = 270

    angle_to_run = []
    negative_angle = offset_angle - 15
    angle_to_run.append(negative_angle)
    positive_angle = offset_angle + 15
    angle_to_run.append(positive_angle)

    # Assume we want to go north
    for item in angle_to_run:
        # print(origin)
        new_point = origin[:]
        # need this splice as issues with value / reference
        # since origin is an object, without the [:] it points to a memory point #! I believe the proper way is to use copy()
        # which varies while new_point is changed (since it related to origin explicitly)
        adj = math.cos(math.radians(item)) * half_radius_deg

        new_point[0] += adj
        opp = math.sin(math.radians(item)) * half_radius_deg

        new_point[1] += opp
        coord_points.append(new_point)

    return coord_points


def getGmapsDirections(origin: coordinates, destination: coordinates, waypoints: list[coordinates]) -> str:
    directions = gmaps.directions(
        origin, destination, waypoints=waypoints, mode="walking"
    )
    # with open("directions.json", "w+") as json_file:
    #    json.dump(directions, json_file, indent = 4, sort_keys=True)
    return directions


def distanceBetweenCoords(lat1: latitude, lon1: longitude, lat2: latitude, lon2: longitude) -> kilometers:
    R = 6378.137
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * \
        math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d


def makeVisitAttractions(waypoints: list[coordinates], attractions: list[coordinates], maxConnectDistance: kilometers) -> list[coordinates]:
    """Updates waypoints along a journey to visit nearby attractions where each attraction has to be within maxConnectDistance of a waypoint"""
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

    return newWaypoints

# test cases
#startEnd = [40.714224, -73.961452]
#midpoints = [[40.71871555587496, -73.961452], [40.714224, -73.95696044412504]]
#attractions = [[40.71847869766016, -73.96370918121455], [40.71851040694706, -73.9604272356968]]

#print(makeVisitAttractions(midpoints, attractions, 1))
