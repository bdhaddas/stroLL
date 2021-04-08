import json

#json.loads(str of JSON)

def getPolyline(data):
    #jsonOutput = json.loads(data) # was json.loads(data) but apparently, gmaps.directions returns a list
    try:
        polyline = data[0]["overview_polyline"]["points"]
        return polyline
    except:
        return ''


