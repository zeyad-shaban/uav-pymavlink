# using potential field method
from pymavlink import mavutil, mavwp
from utils import readlatlongalt, getDistance2Points, wpAroundObstacle
import math

safetyMargin = 0
pointsAroundObs = 1

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

wpCords = readlatlongalt('./wdronekit/Waypoints.csv')
obsCords = readlatlongalt('./wdronekit/Obstacles.csv')

newCords = []
i = 0
for wp in wpCords:
    for obs in obsCords:
        if getDistance2Points(wp[0], wp[1], obs[0], obs[1]) <= obs[2] + safetyMargin:
            for aroundObs in wpAroundObstacle(wp, obs, safetyMargin, pointsAroundObs):
                i += 1
                newCords.append(aroundObs)
        else:
            newCords.append(wp)

for i, cord in enumerate(newCords):
    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
        cord[0], cord[1], cord[2]))


master.waypoint_clear_all_send()
master.waypoint_count_send(wpLoader.count())

for i in range(wpLoader.count()):
    msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
    master.mav.send(wpLoader.wp(msg.seq))
