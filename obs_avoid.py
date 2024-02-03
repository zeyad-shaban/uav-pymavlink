# TODO OPTIMIZE
from pymavlink import mavutil, mavwp
from utils import readlatlongaltFile, getDistance2Points, getBearing2Points, new_waypoint
import math

from UAV import UAV
myUav = UAV('./wdronekit/Data.json')

safetyMargin = 0
pointsAroundObs = 1

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

wpCords = readlatlongaltFile('./testmission.csv')
obsCords = readlatlongaltFile('./testobstacle.csv')


def add_avoid_waypoint(latA, longA, altA, latB, longB, altB, obsLat, obsLong, obsRad, obsBearing, execludeObsI):
    dObs = obsRad * myUav.safe_dist

    latNew, longNew = new_waypoint(obsLat, obsLong, dObs, obsBearing)
    check_2nd_time(latA, longA, altA, latNew, longNew, altA, execludeObsI)
    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, execludeObsI, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
        latNew, longNew, altA))
    check_2nd_time(latNew, longNew, altA, latB, longB, altB, execludeObsI)


def check_2nd_time(latA, longA, altA, latB, longB, altB, execludeObsI):
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

        if not ((brng <= 270 and brng >= 90) or (L >= (myUav.safe_dist * ObsRad)) or (distance_a_obs > distance_a_b)):
            add_avoid_waypoint(latA, longA, altA, latB, longB, altB, ObsLat, ObsLong, ObsRad, bearingObs, i)


if len(obsCords) == 0:
    for i, wp in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            wp[0], wp[1], wp[2]))

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
            obsRadius = math.sqrt(obs[2]**2 + nextObs[2]**2)  # obs[2] + nextObs[2]
            obsCords[i] = [ObsLat_new, ObsLong_new, obsRadius]
            del obsCords[i+1]
        else:
            i += 1

    for i, wp in enumerate(wpCords[:-1]):
        nextWp = wpCords[i+1]
        latA, longA, altA = wp[0], wp[1], wp[2]
        latB, longB, altB = nextWp[0], nextWp[1], nextWp[2]

        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            latA, longA, altA))
        check_2nd_time(latA, longA, altA, latB, longB, altB, None)
        # for j, obs in enumerate(obsCords):
        #     ObsLat, ObsLong, ObsRad = obs[0], obs[1], obs[2]
        #     dAB = getDistance2Points(LatA, LongA, LatB, LongB)
        #     dAob = getDistance2Points(LatA, LongA, ObsLat, ObsLong)
        #     brngAB = getBearing2Points(LatA, LongA, LatB, LongB)
        #     brngobs = brngAB - 90
        #     brngAob = getBearing2Points(LatA, LongA, ObsLat, ObsLong)

        #     if brngAB > brngAob:
        #         brng = brngAB - brngAob
        #     else:
        #         brng = brngAob - brngAB

        #     L = dAob * math.sin(brng*(math.pi/180))

        #     if not ((brng <= 270 and brng >= 90) or (L >= (myUav.safe_dist * ObsRad)) or (dAob > dAB)):
        #         add_avoid_waypoint(LatA, LongA, AltA, LatB, LongB, AltB, ObsLat, ObsLong, ObsRad, brngobs, j)

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
        latB, longB, altB))


# master.waypoint_clear_all_send()
# master.waypoint_count_send(wpLoader.count())

# for i in range(wpLoader.count()):
#     msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
#     master.mav.send(wpLoader.wp(msg.seq))
