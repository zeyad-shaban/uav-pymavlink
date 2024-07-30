# TODO TEST
from modules.utils import getDistance2Points, getBearing2Points, new_waypoint, writeMissionPlannerFile, readWaypoints
import math
from geopy.distance import geodesic
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    # Calculate the great-circle distance between two points on the Earth's surface.
    R = 6371000  # Earth radius in meters
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

def is_obstacle_between(pointA, pointB, obstacle, radius):
    # Extract coordinates
    pointA_lat, pointA_long = pointA
    pointB_lat, pointB_long = pointB
    obstacle_lat, obstacle_long = obstacle

    # Convert coordinates to Cartesian (X, Y) for easier calculations
    def latlon_to_xy(lat, lon):
        return (lat, lon)
    
    Ax, Ay = latlon_to_xy(pointA_lat, pointA_long)
    Bx, By = latlon_to_xy(pointB_lat, pointB_long)
    Ox, Oy = latlon_to_xy(obstacle_lat, obstacle_long)

    # Vector AB and AO
    AB = np.array([Bx - Ax, By - Ay])
    AO = np.array([Ox - Ax, Oy - Ay])
    
    # Project AO onto AB to find the closest point on the line segment
    AB_squared = np.dot(AB, AB)
    if AB_squared == 0:
        return False  # A and B are the same point
    
    AO_dot_AB = np.dot(AO, AB)
    t = AO_dot_AB / AB_squared
    t = max(0, min(1, t))  # Clamp t to the range [0, 1]

    # Find the projection point
    projection = np.array([Ax, Ay]) + t * AB

    # Distance from the obstacle to the projection point
    distance_to_obstacle = haversine(projection[0], projection[1], obstacle_lat, obstacle_long)

    return distance_to_obstacle <= radius


safetyMargin = 0
pointsAroundObs = 1


def ObstacleAvoid(uav, wpPath, obsPath):
    wpCords = readWaypoints(wpPath)

    obsCords = [] if obsPath is None else readWaypoints(obsPath)
    newWaypoints = []

    def add_avoid_waypoint(latA, longA, altA, latB, longB, altB, obsLat, obsLong, obsRad, obsBearing, execludeObsI):
        dObs = obsRad + uav.safe_dist

        latNew, longNew = new_waypoint(obsLat, obsLong, dObs, obsBearing)
        # check_obstacles(latA, longA, altA, latNew, longNew, altA, execludeObsI)
        newWaypoints.append([latNew, longNew, altA])
        # check_obstacles(latNew, longNew, altA, latB, longB, altB, execludeObsI)

    def check_obstacles(latA, longA, altA, latB, longB, altB, execludeObsI):
        for i, obs in enumerate(obsCords):
            if execludeObsI is not None and i == execludeObsI:
                continue

            ObsLat, ObsLong, ObsRad = obs

            is_obstacle_between([latA, longA], [latB, longB], [ObsLat, ObsLong], ObsRad + uav.safe_dist)
            distance_a_b = getDistance2Points(latA, longA, latB, longB)
            distance_a_obs = getDistance2Points(latA, longA, ObsLat, ObsLong)
            bearing_a_obs = getBearing2Points(latA, longA, ObsLat, ObsLong)
            bearing_a_b = getBearing2Points(latA, longA, latB, longB)
            bearingObs = bearing_a_b - 90

            if bearing_a_b > bearing_a_obs:
                brng = bearing_a_b - bearing_a_obs
            else:
                brng = bearing_a_obs - bearing_a_b

            obsAffects = is_obstacle_between([latA, longA], [latB, longB], [ObsLat, ObsLong], ObsRad + uav.safe_dist)
            if (obsAffects):
                add_avoid_waypoint(latA, longA, altA, latB, longB, altB, ObsLat, ObsLong, ObsRad, bearingObs, i)

    if len(obsCords) == 0:
        for i, wp in enumerate(wpCords):
            newWaypoints.append([wp[0], wp[1]])

    else:
        # combine close obstacles
        i = 0
        while i < len(obsCords) - 1:
            obs = obsCords[i]
            nextObs = obsCords[i+1]
            distance = getDistance2Points(obs[0], obs[1], nextObs[0], nextObs[1])
            bearing = getBearing2Points(obs[0], obs[1], nextObs[0], nextObs[1])
            if abs(distance) <= 30:
                ObsLat_new, ObsLong_new = new_waypoint(obs[0], obs[1], distance / 2, bearing)
                # ! TEST THE NEW RADIUS IMPLEMENTATION INSTEAD OF JUST ADDING
                obsRadius = obs[2] + nextObs[2]  # math.sqrt(obs[2]**2 + nextObs[2]**2)
                obsCords[i] = [ObsLat_new, ObsLong_new, obsRadius]
                del obsCords[i+1]
            else:
                i += 1

        firstWp = wpCords[0]
        newWaypoints.append([firstWp[0], firstWp[1], uav.alt])
        for i, wp in enumerate(wpCords[:-1]):
            nextWp = wpCords[i+1]
            latA, longA, altA = wp[0], wp[1], uav.alt
            latB, longB, altB = nextWp[0], nextWp[1], uav.alt

            check_obstacles(latA, longA, altA, latB, longB, altB, None)

            newWaypoints.append([latB, longB, altB])

    writeMissionPlannerFile(newWaypoints, './data/AVOIDED_WP.waypoints')

    return newWaypoints
