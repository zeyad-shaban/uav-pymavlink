from pymavlink import mavutil, mavwp
from wpymavlink.ObstacleAvoid import ObstacleAvoid
import modules.utils as utils
from modules.UAV import UAV
myUav = UAV('./wdronekit/Data.json')

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

wpCords = ObstacleAvoid('./wdronekit/Waypoints.csv', './wdronekit/Obstacles.csv')

home = wpCords[0]



def takeoffSequence():
    lat, long = utils.new_waypoint(home[0], home[1], 1, myUav.main_bearing)
    wpLoader.insert(1, mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0,
        lat, long, 1
    ))

def loadWaypoints():
    for i, cord in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], cord[2]))

def landingSequence():
    start_land_dist = 100
    loiter_alt = 20
    loiter_lat, loiter_long = utils.new_waypoint(home[0], home[1], start_land_dist, myUav.main_bearing-180)

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0,
        loiter_lat, loiter_long, loiter_alt
    ))


def calculateGrid():
    print("hello")

polygon = [[lat1, lon1], [lat2, lon2], [lat3, lon3], [lat4, lon4]]

grid_points = calculate_grid_points(polygon)

for i, (lat, lon) in enumerate(grid_points):
    waypoint = mavutil.mavlink.MAVLink_mission_item_message(
        mavlink_connection.target_system, mavlink_connection.target_component,
        seq=i, frame=mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        command=mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        current=0, autocontinue=1,
        param1=0, param2=0, param3=0, param4=0,
        x=lat, y=lon, z=altitude
    )

    # Send the waypoint
    mavlink_connection.mav.send(waypoint)


master.waypoint_clear_all_send()
master.waypoint_count_send(wpLoader.count())

for i in range(wpLoader.count()):
    msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
    master.mav.send(wpLoader.wp(msg.seq))
