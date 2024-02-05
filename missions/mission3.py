from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint
from modules.ObstacleAvoid import ObstacleAvoid
from modules.Fence import uploadFence

def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    def addHome():
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        home = [msg.lat / 1e7, msg.lon / 1e7]

        mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            home[0], home[1], 0)

        return home

    def takeoffSequence(home):
            lat, long = new_waypoint(home[0], home[1], 1, uav.main_bearing)
            wpLoader.insert(1, mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0,
                lat, long, 1
            ))

    def landingSequence(home):
        start_land_dist = 100
        loiter_alt = 20
        loiter_lat, loiter_long = new_waypoint(home[0], home[1], start_land_dist, uav.main_bearing-180)

        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0,
            loiter_lat, loiter_long, loiter_alt
        ))

    cords = ObstacleAvoid(uav, './data/Waypoints.csv', './data/Obstacles.csv')
    uploadFence(master, './data/Geofence.csv')