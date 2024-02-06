# MISSION PLANNER SOURCE CODE HOLLY HECK: https://github.com/ArduPilot/MissionPlanner/tree/c19b4fae19e41f5da5dba91d1b5ab1ed0efe9dbd/ExtLibs/SimpleGrid
from pymavlink import mavutil, mavwp
from modules.utils import addHome, takeoffSequence, landingSequence, readMissionPlannerFile
from modules.ObstacleAvoid import ObstacleAvoid
from modules.Fence import uploadFence


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    uploadFence(master, './data/Geofence.csv')

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)

    cords = readMissionPlannerFile('./data/SearchGrid.txt')
    for i, cord in enumerate(cords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i+2, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            float(cord[0]), float(cord[1]), float(cord[2])))

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for i in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))
