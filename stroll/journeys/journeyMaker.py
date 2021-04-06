import googlemaps
from datetime import datetime
import json
import objectpath
import math

gmaps = googlemaps.Client(key='')

def coord_radial(origin, radius, compassDirection): #? generateRadialPath(origin
    radius_deg = radius/111.32
    half_radius_deg = radius_deg/2
    coord_points = []
    offset_angle = 0
    if compassDirection == 'North':
        offset_angle = 0
    elif compassDirection == 'East':
        offset_angle = 90
    elif compassDirection == 'South':
        offset_angle = 180
    elif compassDirection == 'West':
        offset_angle = 270  

    angle_to_run = []
    negative_angle = offset_angle - 15
    angle_to_run.append(negative_angle)
    positive_angle = offset_angle + 15 
    angle_to_run.append(positive_angle)

    #Assume we want to go north    
    for item in angle_to_run:
        # print(origin)
        new_point = origin[:]
        # need this splice as issues with value / reference
        # since origin is an object, without the [:] it points to a memory point
        # which varies while new_point is changed (since it related to origin explicitly)
        adj = math.cos(math.radians(item))*half_radius_deg

        new_point[0] += adj
        opp = math.sin(math.radians(item))*half_radius_deg

        new_point[1] += opp
        coord_points.append(new_point)

    return coord_points

def get_directions(origin, destination, midpoint):
    directions = gmaps.directions(origin, destination, waypoints=midpoint, mode="walking")
    #with open("directions.json", "w+") as json_file:
    #    json.dump(directions, json_file, indent = 4, sort_keys=True)
    return directions
