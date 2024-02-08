from missions import mission1, mission2, mission3
from modules.UAV import UAV
from modules.Camera import Camera

if __name__ == "__main__":
    uav = UAV("./data/Data.json")
    connectionString = "udpin:172.26.240.1:14550"

    sonya6000 = Camera(spacingAt100Alt=47, focalLength=20, imgWidth=6000, imgHeight=4000, sensorWidth=23.5, sensorHeight=15.6)
    goProHero4Black = Camera(spacingAt100Alt=100.33, focalLength=2.5, imgWidth=40000, imgHeight=3000, sensorWidth=6.17, sensorHeight=4.56) # ! in the code focal length was 2.94, in mission planner it is 2.5

    # mission1.startMission(uav, connectionString, payloadRadius=0) # 0 radius means default
    mission2.startMission(uav, connectionString, sonya6000, surveyAlt=80, surveySpeed=20)
