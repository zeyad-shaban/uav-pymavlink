# MISSION PLANNER SOURCE CODE HOLLY HECK: https://github.com/ArduPilot/MissionPlanner/tree/c19b4fae19e41f5da5dba91d1b5ab1ed0efe9dbd/ExtLibs/SimpleGrid
from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint, addHome, takeoffSequence, landingSequence, readlatlongFile
from modules.ObstacleAvoid import ObstacleAvoid
from modules.Fence import uploadFence


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    uploadFence(master, './data/Geofence.csv')

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)

    squareCords = readlatlongFile('./data/Square.csv')
    print(squareCords)

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for i in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))
