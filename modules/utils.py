import math
from typing import List
from pymavlink import mavutil
from modules.UAV import UAV

R = 6371000.0  # Earth radius in meters


def readWaypoints(path: str) -> List[List[float]]:
    with open(path) as f:
        firstLine = next(f)
        cords = []
        for line in f:
            if firstLine.startswith("n,lat,long"):
                line = line.split(",")
                cords.append([float(line[0]), float(line[1]), 0])
            elif firstLine.startswith('n,lat,long,alt') or firstLine.startswith('n,lat,lon,radius'):
                line = line.split(",")
                cords.append([float(line[0]), float(line[1]), float(line[2])])
            elif firstLine.startswith("QGC WPL 110"):
                line = line.split('\t')
                cords.append([float(line[8]), float(line[9]), float(line[10])])

            else:
                print(f'!!!!!!"FILE FORMAT NOT SUPPORTED {firstLine}!!!!!!!!!!!')
                return []

        return cords


def writeMissionPlannerFile(wpCords, path):
    with open(path, 'w') as f:
        f.write("QGC WPL 110\n")
        for i, cord in enumerate(wpCords):
            cmd = 16
            if i == 1:
                cmd = 22
            elif i == len(wpCords) - 1:
                cmd = 21

            f.write("{}\t{}\t{}\t{}\t0.00000000\t0.00000000\t0.00000000\t0.00000000\t{}\t{}\t{}\t1\n".format(i, int(i == 0), 0 if i == 0 else 3, cmd, cord[0], cord[1], cord[2]))


def new_waypoint(lat1, long1, d, brng):
    brng *= math.pi/180
    lat1, long1 = math.radians(lat1), math.radians(long1)
    lat2_r = math.asin(math.sin(lat1) * math.cos(d / R) + math.cos(lat1) * math.sin(d / R) * math.cos(brng))
    long2_r = long1 + math.atan2((math.sin(brng) * math.sin(d / R) * math.cos(lat1)), (math.cos(d / R) - math.sin(lat1) * math.sin(lat2_r)))
    return math.degrees(lat2_r), math.degrees(long2_r)


def printfile(aFileName):  # Print a mission file to demonstrate "round trip"
    print("\nMission file: %s" % aFileName)
    with open(aFileName) as f:
        for line in f:
            print(' %s' % line.strip())


def getDistance2Points(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km * 1000


def getBearing2Points(lat1, long1, lat2, long2):
    lat1, long1 = math.radians(lat1), math.radians(long1)
    lat2, long2 = math.radians(lat2), math.radians(long2)
    y = math.sin(long2 - long1) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(long2 - long1)
    i = math.atan2(y, x)
    return (i * 180 / math.pi + 360) % 360


def addHome(master, wpLoader):
    msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
    home = [msg.lat / 1e7, msg.lon / 1e7]

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
        home[0], home[1], 0))

    return home


def takeoffSequence(master, wpLoader, home, uav):
    lat, long = new_waypoint(home[0], home[1], 1, uav.main_bearing)
    wpLoader.insert(1, mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0,
        lat, long, 1
    ))


def landingSequence(master, wpLoader, home, uav: UAV):
    start_land_dist = 100
    loiter_alt = 20
    loiter_rad = 50
    loiter_lat, loiter_long = new_waypoint(home[0], home[1], start_land_dist, uav.main_bearing-180)

    wpLoader.add(
        mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 1, 0, loiter_rad, 0, 0,
            loiter_lat, loiter_long, loiter_alt)
    )

    wpLoader.add(
        mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0,
            home[0], home[1], 0)
    )
