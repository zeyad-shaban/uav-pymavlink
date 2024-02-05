from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()


def readlatlongFile(path):
    with open(path) as f:
        if not next(f).startswith("n,lat,long"):
            return print("File not supported (must be n,lat,long)")

        cords = []
        for line in f:
            line = line.split(",")
            cords.append([float(line[0]), float(line[1])])

        return cords



squareCorners = readlatlongFile('./square.txt')

print(squareCorners)

