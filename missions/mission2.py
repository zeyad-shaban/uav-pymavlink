import os
import glob
from typing import List
import math
from pymavlink import mavutil, mavwp
from modules.utils import addHome, takeoffSequence, landingSequence, readWaypoints, getBearing2Points, new_waypoint, getDistance2Points
from modules.Fence import uploadFence
from modules.RectPoints import RectPoints
from modules.ImageDetector import openCam, closeCam
from modules.UAV import UAV
from modules.Camera import Camera

from modules.ObstacleAvoid import ObstacleAvoid
# import time


def startMission(uav: UAV, master, wpPath, fencePath, obsPath, camera: Camera, surveyAlt: float, surveySpeed: float, surveySquarePath) -> None:
    camera.adjutSpacingToAlt(surveyAlt)
    wpLoader = mavwp.MAVWPLoader()

    uploadFence(master, fencePath)

    home = addHome(master, wpLoader, uav)
    wpCords = ObstacleAvoid(uav, wpPath, obsPath)
    # takeoffSequence(master, wpLoader, home, uav)

    for i, cord in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], uav.alt))

    recCords = readWaypoints(surveySquarePath)
    searchRec = RectPoints(*recCords)

    cords = generateSurveyFromRect(searchRec, camera.spacing, wpCords[-1])
    for i, cord in enumerate(cords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i+2, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            float(cord[0]), float(cord[1]), surveyAlt))
        if i == 0:
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system,  # target system
                mavutil.mavlink.MAV_COMP_ID_SYSTEM_CONTROL,  # target component
                0,  # sequence number
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # frame
                mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,  # command
                0,  # current
                1,  # autocontinue
                0,  # param1 (type of speed: 0=airspeed, 1=ground speed)
                surveySpeed,  # param2 (target speed, in m/s)
                0, 0, 0, 0, 0  # param3, param4, param5, param6, param7 (not used)
            ))

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for i in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))

    # didOpenCam = False
    # didCloseCam = False
    # while True:
    #     msg = master.recv_match(type='MISSION_ITEM_REACHED', blocking=True)
    #     if msg.seq >= 2 and not didOpenCam:
    #         openCam()
    #         didOpenCam = True
    #     elif msg.seq > len(cords) + 1 and not didCloseCam:
    #         closeCam()
    #         didCloseCam = True
    #         break


def generateSurveyFromRect(rec: RectPoints, spacing, planeLocation) -> List[List[float]]:
    points = []
    closestPoint = rec.getClosestPoint(planeLocation)
    furthestConnectedPoint = rec.getFurthestConnectedPoint(closestPoint)

    travelBearing = getBearing2Points(*closestPoint, *furthestConnectedPoint)
    travelDistance = getDistance2Points(*closestPoint, *furthestConnectedPoint)

    rotatePoint2 = [point for point in rec.getConnectedPoints(furthestConnectedPoint) if point != closestPoint][0]
    rotateBearing = getBearing2Points(*furthestConnectedPoint, *rotatePoint2)
    uncoveredDistance = getDistance2Points(*furthestConnectedPoint, *rotatePoint2)

    lastPoint = closestPoint
    rotateToggle = False
    direction = 0

    while uncoveredDistance > 0:
        points.append(lastPoint)

        if rotateToggle:
            lastPoint = new_waypoint(*lastPoint, spacing, rotateBearing)
            uncoveredDistance -= spacing
            direction += 180
            rotateToggle = False
        else:
            lastPoint = new_waypoint(*lastPoint, travelDistance, travelBearing + direction)
            rotateToggle = True

    return points


# TODO USE THIS AND HANDLE SAVING THE PLANE CORDS TO KNOW WHERE THE PLANE IS LOCATED
def saveGeoCord(camera: Camera, master, cords: List[float]) -> None:
    with open("./data/Geoloc.txt", 'a') as f:
        xCord = cords[0]  # x
        yCord = cords[1]  # y

        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)

        centerPixel = [2000, 1500]

        pixels_width = abs(float(centerPixel[0]) - float(xCord))
        pixels_length = abs(float(centerPixel[1]) - float(yCord))

        gsdw = float(((msg.alt / 1e3) * camera.sensorWidth) / (camera.focalLength*4000))
        gsdl = float(((msg.alt / 1e3) * camera.sensorHeight) / (camera.focalLength*3000))
        land_width = gsdw*pixels_width
        land_length = gsdl*pixels_length
        distance = math.sqrt(((land_width)**2) + ((land_length)**2))  # distance in meters

        d1 = centerPixel[0] - int(xCord)
        d2 = centerPixel[1] - int(yCord)

        if d1 >= 0 and d2 >= 0:  # First quad
            angle = math.degrees(math.atan(d1/d2))

        elif d1 <= 0 and d2 >= 0:  # second quad
            d2 = -d2
            angle = 360 - math.degrees(math.atan(d1/d2))

        elif d1 <= 0 and d2 <= 0:  # Third quad
            angle = 270 - math.degrees(math.atan(d2/d1))

        else:
            d2 = -d2
            angle = 180 - math.degrees(math.atan(d1/d2))

        bearing = 0
        Angle = bearing - angle

        image_x2, image_y2 = new_waypoint(msg.lat / 1e7, msg.lon / 1e7, distance, Angle)

        f.truncate()
        f.write(f"{str(image_x2)},{str(image_y2)}\n")
