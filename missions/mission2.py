# MISSION PLANNER SOURCE CODE HOLLY HECK: https://github.com/ArduPilot/MissionPlanner/tree/c19b4fae19e41f5da5dba91d1b5ab1ed0efe9dbd/ExtLibs/SimpleGrid
import os
import glob
from pymavlink import mavutil, mavwp
from modules.utils import addHome, takeoffSequence, landingSequence, createSquareFromMidpoint, generateSurveyFromRect
from modules.Fence import uploadFence
from modules.RectPoints import RectPoints
from modules.ImageDetector import shouldCapture

import cv2
# import time


# ! make sure this will work with pixahawk as the host of the camera, if not need to look at video_start_stream and video_end_stream
def startCam():
    dir_path = "./images"
    os.makedirs(dir_path, exist_ok=True)
    files = glob.glob(f"{dir_path}/*.png")

    lastIndex = 0
    if files:
        # to prevent anything from being accidently deleted if the python code reran again
        max_number = max(int(os.path.splitext(os.path.basename(file))[0]) for file in files)
        lastIndex = max_number + 1

    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("!!!!!FRAME NOT READ CORRECTLY!!!!!")
            break

        if shouldCapture(frame):
            cv2.imwrite(f'./images/{lastIndex}.png', frame)
            lastIndex += 1
            # time.sleep(0.5) # needed only if ai team didn't handle the delay

    cap.release()


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    surveyAlt = 80
    midpointCords = [29.8145362, 30.8257806]
    surveyDistance = 200  # in meters
    surveySpacing = 10  # in meters

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

    # ? should we make it auto shutdown after the plane is disarmed or ctrl+c is enough this is enough?
    startCam()
