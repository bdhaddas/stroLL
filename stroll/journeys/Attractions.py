import json

#json.loads(str of JSON)

def getPolyline(data):
    json = json.loads(data)
    polyline = json[0]["overview_polyline"]["points"]
    return polyline

