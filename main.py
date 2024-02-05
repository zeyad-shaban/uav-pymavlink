from missions import mission1, mission3
from modules.UAV import UAV

if __name__ == "__main__":
    uav = UAV("./data/Data.json")
    connectionString = "udpin:172.26.240.1:14550"

    mission3.startMission(uav, connectionString)