from pymavlink import mavutil
from missions import mission1, mission2, mission3
from missions import mission1
from modules.UAV import UAV
from modules.Camera import Camera


if __name__ == "__main__":
    MISSION_NUMBER = 1

    uav = UAV("./data/Data.json")
    connectionString = "udpin:172.24.128.1:14550"
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()

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
        mission2.startMission(uav, master, sonya6000, surveyAlt=80, surveySpeed=10, surveySquarePath=surveySquare, fencePath=fencePath)
    elif MISSION_NUMBER == 3:
        mission3.startMission(uav, master, wpPath=wpPath, obsPath=obsPath, fencePath=fencePath)
