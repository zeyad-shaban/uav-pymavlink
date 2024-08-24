from pymavlink import mavutil
from missions import mission1, mission2, mission3
from missions import mission1
from modules.UAV import UAV
from modules.Camera import Camera


if __name__ == "__main__":
    MISSION_NUMBER = 1

    uav = UAV("./data/Data.json")
    connectionString = "172.29.48.1:14550"
    print("connecting")
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    print("connected")

    sonya6000 = Camera(spacingAt100Alt=47, focalLength=20, imgWidth=6000, imgHeight=4000, sensorWidth=23.5, sensorHeight=15.6)
    goProHero4Black = Camera(spacingAt100Alt=100.33, focalLength=2.94, imgWidth=40000, imgHeight=3000, sensorWidth=6.17, sensorHeight=4.56)  # old code focal length was 2.94, mp: 2.5

    wpPath = './data/Waypoints.csv'
    obsPath = './data/Obstacles.csv'
    payloadPath = './data/Payloads.csv'
    fencePath = './data/Geofence.csv'
    surveySquare = './data/SearchSquare.csv'

    if MISSION_NUMBER == 1:
        mission1.startMission(uav, master, wpPath=wpPath, fencePath=fencePath, obsPath=obsPath, payloadPath=payloadPath, payloadRadius=10)  # 0 radius means default
    elif MISSION_NUMBER == 2:
        mission2.startMission(uav, master, wpPath=wpPath, fencePath=fencePath, obsPath=obsPath, camera=sonya6000, surveyAlt=60, surveySpeed=20, surveySquarePath=surveySquare)
    elif MISSION_NUMBER == 3:
        mission3.startMission(uav, master, wpPath=wpPath, obsPath=obsPath, fencePath=fencePath)


# steps for running during flight test:
#   1. set fence_total parameter to needed
#   2. Set the home lat, long in uav.py (or let the gps decide it, but this can get somewhat risky if the gps messed up the bytes)