# TODO TEST
from modules.utils import getDistance2Points, getBearing2Points, new_waypoint, writeMissionPlannerFile, readWaypoints
import math

safetyMargin = 0
pointsAroundObs = 1


def ObstacleAvoid(uav, wpPath, obsPath):
    wpCords = readWaypoints(wpPath)

    obsCords = [] if obsPath is None else readWaypoints(obsPath)
    newWaypoints = []

    def add_avoid_waypoint(latA, longA, altA, latB, longB, altB, obsLat, obsLong, obsRad, obsBearing, execludeObsI):
        dObs = obsRad + uav.safe_dist

        latNew, longNew = new_waypoint(obsLat, obsLong, dObs, obsBearing)
        check_obstacles(latA, longA, altA, latNew, longNew, altA, execludeObsI)
        newWaypoints.append([latNew, longNew, altA])
        check_obstacles(latNew, longNew, altA, latB, longB, altB, execludeObsI)

    def check_obstacles(latA, longA, altA, latB, longB, altB, execludeObsI):
        for i, obs in enumerate(obsCords):
            if execludeObsI is not None and i == execludeObsI:
                continue

            ObsLat, ObsLong, ObsRad = obs
            distance_a_b = getDistance2Points(latA, longA, latB, longB)
            distance_a_obs = getDistance2Points(latA, longA, ObsLat, ObsLong)
            bearing_a_obs = getBearing2Points(latA, longA, ObsLat, ObsLong)
            bearing_a_b = getBearing2Points(latA, longA, latB, longB)
            bearingObs = bearing_a_b - 90

            if bearing_a_b > bearing_a_obs:
                brng = bearing_a_b - bearing_a_obs
            else:
                brng = bearing_a_obs - bearing_a_b

            L = distance_a_obs * math.sin(brng*(math.pi/180))

            if not ((brng <= 270 and brng >= 90) or (L >= (uav.safe_dist * ObsRad)) or (distance_a_obs > distance_a_b)):
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

        for i, wp in enumerate(wpCords[:-1]):
            nextWp = wpCords[i+1]
            latA, longA, altA = wp[0], wp[1], uav.alt
            latB, longB, altB = nextWp[0], nextWp[1], uav.alt

            newWaypoints.append([latA, longA, altA])
            check_obstacles(latA, longA, altA, latB, longB, altB, None)

            newWaypoints.append([latB, longB, altB])

    writeMissionPlannerFile(newWaypoints, './data/AVOIDED_WP.waypoints')

    return newWaypoints
