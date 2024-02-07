# MISSION PLANNER SOURCE CODE HOLLY HECK: https://github.com/ArduPilot/MissionPlanner/tree/c19b4fae19e41f5da5dba91d1b5ab1ed0efe9dbd/ExtLibs/SimpleGrid
from pymavlink import mavutil, mavwp
from modules.utils import addHome, takeoffSequence, landingSequence, createSquareFromMidpoint, generateSurveyFromRect
from modules.Fence import uploadFence
from modules.RectPoints import RectPoints


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    surveyAlt = 80
    midpointCords = [29.8145362, 30.8257806]
    surveyDistance = 1000 # in meters
    surveySpacing = 10 # in meters

    uploadFence(master, './data/Geofence.csv')

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)

    squarePoints: RectPoints = createSquareFromMidpoint(midpointCords, surveyDistance)
    # uncomment below to visualize the square
    # cords = [
    #     [squarePoints.topLeft[0], squarePoints.topLeft[1]],
    #     [squarePoints.topRight[0], squarePoints.topRight[1]],
    #     [squarePoints.bottomRight[0], squarePoints.bottomRight[1]],
    #     [squarePoints.bottomLeft[0], squarePoints.bottomLeft[1]],
    # ]
    cords = generateSurveyFromRect(squarePoints, surveySpacing)
    for i, cord in enumerate(cords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i+2, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            float(cord[0]), float(cord[1]), surveyAlt))

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for i in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))