import os
import glob
from typing import List
from pymavlink import mavutil, mavwp
from modules.utils import addHome, takeoffSequence, landingSequence, readlatlongFile, getBearing2Points, new_waypoint, getDistance2Points
from modules.Fence import uploadFence
from modules.RectPoints import RectPoints
from modules.ImageDetector import shouldCapture
from modules.UAV import UAV
from modules.Camera import Camera

import cv2
# import time


def startMission(uav: UAV, connectionString: str, camera: Camera) -> None:
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    surveyAlt = 80
    camera.adjutSpacingToAlt(surveyAlt)

    uploadFence(master, './data/Geofence.csv')

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)

    try:
        recCords = readlatlongFile('./data/SearchSquare.csv')
    except FileNotFoundError:
        recCords = readlatlongFile('./data/defaults/SearchSquare.csv')

    searchRec = RectPoints(*recCords)

    cords = generateSurveyFromRect(searchRec, camera.spacing, home)
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

    startCam()

# TODO change plane speed
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


# ! make sure this will work with pixahawk as the host of the camera, if not need to look at video_start_stream and video_end_stream
def startCam():
    imgPath = "./images"
    cordsPath = "./data/cords.csv"
    camId = 0

    os.makedirs(imgPath, exist_ok=True)
    files = glob.glob(f"{imgPath}/*.png")

    lastIndex = 0
    if files:
        max_number = max(int(os.path.splitext(os.path.basename(file))[0]) for file in files)
        lastIndex = max_number + 1

    cap = cv2.VideoCapture(camId)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("!!!!!FRAME NOT READ CORRECTLY!!!!!")
            break

        if shouldCapture(frame):
            cv2.imwrite(f'./images/{lastIndex}.png', frame)
            lastIndex += 1

            # time.sleep(0.5) # uncomment only if ai team didn't handle the delay

    cap.release()

# def image_coordinates(uav: UAV, master, camera: Camera):
#     pixelFile = "Pixels"
#     p2List, p2No = robenuav.FileList(pixelFile)
#     with open("Geoloc.txt", 'a') as f:
#         f.seek(0)
#         for x in range(p2No+1):
#             p2 = p2List[x]
#             p2_width = p2['x']
#             p2_length = p2['y']
#             # p2 = [279,272] # random point from AI'S code

#             h_plane = float(vehicle.location.global_frame.alt)  # h_plane=80 #altitude of plane
#             # h_plane = 80
#             w_sensor = 6.17  # width sensor
#             l_sensor = 4.55  # length sensor
#             fl = 2.92  # focal length

#             # Current Locaation
#             lat1 = float(vehicle.location.global_frame.lat)
#             long1 = float(vehicle.location.global_frame.lon)

#             # lat1 = 29.8259667414763
#             # long1 = 31.3282012939453

#             # pixels in image
#             p1 = [2000, 1500]  # center of image

#             pixels_width = abs(float(p1[0]) - float(p2_width))
#             pixels_length = abs(float(p1[1]) - float(p2_length))

#             gsdw = float((h_plane*w_sensor) / (fl*4000))
#             gsdl = float((h_plane*l_sensor) / (fl*3000))
#             land_width = gsdw*pixels_width
#             land_length = gsdl*pixels_length
#             # landwidth = gsdw*1920
#             # landlength = gsdl*1080
#             distance = math.sqrt(((land_width)**2) + ((land_length)**2))  # distance in meters

#             d1 = p1[0] - int(p2_width)
#             d2 = p1[1] - int(p2_length)

#             if d1 >= 0 and d2 >= 0:  # First quad
#                 angle = math.degrees(math.atan(d1/d2))

#             elif d1 <= 0 and d2 >= 0:  # second quad
#                 d2 = -d2
#                 angle = 360 - math.degrees(math.atan(d1/d2))

#             elif d1 <= 0 and d2 <= 0:  # Third quad
#                 angle = 270 - math.degrees(math.atan(d2/d1))

#             else:
#                 d2 = -d2
#                 angle = 180 - math.degrees(math.atan(d1/d2))

#             # bearing = vehicle.heading #Current bearing
#             bearing = 0
#             Angle = bearing - angle

#             image_x2, image_y2 = robenuav.new_waypoint(lat1, long1, distance, Angle)

#             f.truncate()
#             f.write(str(image_x2))
#             f.write(",")
#             f.write(str(image_y2))
#             f.write("\n")
