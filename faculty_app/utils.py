from math import radians, sin, cos, sqrt, atan2

def distance(lat1, lng1, lat2, lng2):
    # approximate radius of earth in km
    R = 6373.0

    # convert degrees to radians
    lat1 = radians(float(lat1))
    lng1 = radians(float(lng1))
    lat2 = radians(float(lat2))
    lng2 = radians(float(lng2))

    # calculate the difference between the latitudes and longitudes
    dlat = lat2 - lat1
    dlng = lng2 - lng1

    # apply the Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance
