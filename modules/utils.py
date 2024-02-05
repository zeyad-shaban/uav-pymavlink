import math
import numpy as np

R = 6371000.0  # Earth radius in meters


def readlatlongFile(path):
    with open(path) as f:
        if not next(f).startswith("n,lat,long"):
            return print("File not supported (must be n,lat,long)")

        cords = []
        for line in f:
            line = line.split(",")
            cords.append([float(line[0]), float(line[1])])

        return cords


def readlatlongaltFile(path):
    with open(path) as f:
        firstLine = next(f)
        if not firstLine.startswith("n,lat,long,alt") and not firstLine.startswith("n,lat,long,radius"):
            return print("File not supported (must be n,lat,long, alt)")

        cords = []
        for line in f:
            line = line.split(",")
            cords.append([float(line[0]), float(line[1]), float(line[2])])

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
    brng = brng * (math.pi/180)
    lat1_r, long1_r = math.radians(lat1), math.radians(long1)
    lat2_r = math.asin(math.sin(lat1_r) * math.cos(d / R) + math.cos(lat1_r) * math.sin(d / R) * math.cos(brng))
    long2_r = long1_r + math.atan2((math.sin(brng) * math.sin(d / R) * math.cos(lat1_r)), (math.cos(d / R) - math.sin(lat1_r) * math.sin(lat2_r)))
    lat2, long2 = math.degrees(lat2_r), math.degrees(long2_r)
    brng = brng * (180/math.pi)
    return lat2, long2


def printfile(aFileName):  # Print a mission file to demonstrate "round trip"
    print("\nMission file: %s" % aFileName)
    with open(aFileName) as f:
        for line in f:
            print(' %s' % line.strip())


def payload_drop_eq(H1, Vpa, Vag, angle):
    g = 9.81  # acceleration due to gravity
    Cd = 0.5  # drag coefficient of payloads
    rho = 1.225  # density of air
    A = 0.02  # average cross section of the payload
    m = 1  # mass of the payload
    H = [float(H1)]  # height of the plane in meters
    ty = [0]  # duration of fall
    Vy = [0]  # velocity in downward direction
    acc = [9.81]  # acceleration in downward direction
    Dy = [0]  # upward drag force
    dy = [0]  # deceleration due to drag force
    k = 1
    int = 0.001  # time intervals for calculation in the loops

    while H[k-1] > 0:
        ty.append(ty[k-1] + int)
        H.append(H[k-1] - (Vy[k-1] * int + 0.5 * acc[k-1] * int**2))
        Vy.append(Vy[k-1] + acc[k-1] * int)
        Dy.append(Cd * rho * (Vy[k-1]**2) * A / 2)
        dy.append(Dy[k-1] / m)
        acc.append(g - dy[k])
        k = k + 1

    print("££££££££££££££££££££££££££££££")
    print("Duration of free-fall:", ty[k-1], "sec")
    print("££££££££££££££££££££££££££££££")

    Vpa = float(Vpa)  # cruising velocity in m/s
    Vag = float(Vag)  # velocity of wind wrt to ground in m/s
    angle = float(angle)  # angle of Vag in degrees

    Vpg = Vpa - Vag * np.cos(np.deg2rad(angle))  # velocity of plane wrt ground
    Vx = [Vpg]  # velocity of payload in horizontal direction
    R = [0]  # distance covered by payload in horizontal direction
    Dx = [Cd * 1.225 * (Vx[0]**2) * A / 2]  # horizontal drag on the payload
    dx = [Dx[0] / m]  # horizontal deceleration on the payload
    k = 1

    Vx = np.append(Vx, np.zeros(len(ty)-1))
    R = np.append(R, np.zeros(len(ty)-1))
    Dx = np.append(Dx, np.zeros(len(ty)-1))
    dx = np.append(dx, np.zeros(len(ty)-1))

    for tx in range(len(ty)-1):
        R[k] = R[k-1] + (Vx[k-1] * int - 0.5 * dx[k-1] * int**2)
        Vx[k] = Vx[k-1] - dx[k-1] * int
        Dx[k] = (Cd*1.225*0.5*A) * (Vx[k] ** 2)
        dx[k] = Dx[k] / m
        k = k + 1

    print("££££££££££££££££££££££££££££££")
    print("Range of payload", (R[k-1]), "meter")
    print("££££££££££££££££££££££££££££££")
    x = R[k-1]
    y = H1
    return x, y


def getDistance2Points(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km * 1000


def getBearing2Points(lat1, long1, lat2, long2):
    lat1_r, long1_r = math.radians(lat1), math.radians(long1)
    lat2_r, long2_r = math.radians(lat2), math.radians(long2)
    y = math.sin(long2_r - long1_r) * math.cos(lat2_r)
    x = math.cos(lat1_r) * math.sin(lat2_r) - math.sin(lat1_r) * math.cos(lat2_r) * math.cos(long2_r - long1_r)
    i = math.atan2(y, x)
    bearing = (i * 180 / math.pi + 360) % 360
    return bearing
