from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint, addHome, takeoffSequence, landingSequence
from modules.ObstacleAvoid import ObstacleAvoid
from modules.Fence import uploadFence


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    wpCords = ObstacleAvoid(uav, './data/Waypoints.csv', './data/Obstacles.csv')
    uploadFence(master, './data/Geofence.csv')

    home = addHome(master)
    takeoffSequence(master, wpLoader, home, uav)

    for i, cord in enumerate(wpCords):
        cmd = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        if i == 1:
            cmd = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF

        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, cmd, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], cord[2]))

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for i in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))
