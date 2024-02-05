from pymavlink import mavutil, mavwp
from time import sleep
from math import sqrt, cos, sin, asin, radians

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()


def getDistance2Points(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km * 1000


cords = [
    [29.81475030, 30.82579140],
    [29.82080080, 30.82585570],
    [29.82093120, 30.83370920],
    [29.81502960, 30.83358050],
]

for i, cord in enumerate(cords):
    cmd = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
    if i == 1:
        cmd = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
    elif i == len(cords) - 1 and False:
        cmd = mavutil.mavlink.MAV_CMD_NAV_LAND

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, cmd, 0, 1, 0, 0, 0, 0,
        cord[0], cord[1], 100))


master.waypoint_clear_all_send()
master.waypoint_count_send(wpLoader.count())

for i in range(wpLoader.count()):
    msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
    master.mav.send(wpLoader.wp(msg.seq))


master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mavutil.mavlink.PLANE_MODE_AUTO
)
master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

insertNow = input("Press enter if you FOUND OBSTACLE AAAAA")

avoidingWpCords = [29.82444960, 30.82976100, 100]


def reachedWPCheck(target_lat, target_lon, acceptance_radius=100):
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    distance = getDistance2Points(target_lat, target_lon, msg.lat / 1e7, msg.lon / 1e7)
    return distance < acceptance_radius


def movePlaneTo(lat, lon, alt):
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.PLANE_MODE_GUIDED
    )
    master.mav.mission_item_send(
        master.target_system,
        master.target_component,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        2, 0, 0, 0, 0, 0,
        lat, lon, alt
    )

    while not reachedWPCheck(lat, lon, 100):
        sleep(0.05)

    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mavutil.mavlink.PLANE_MODE_AUTO
    )


movePlaneTo(avoidingWpCords[0], avoidingWpCords[1], avoidingWpCords[2])
