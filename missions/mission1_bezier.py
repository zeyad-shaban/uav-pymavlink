from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint, readWaypoints, addHome, takeoffSequence, landingSequence, getBearing2Points, isPointInFence, getDistance2Points
import numpy as np
from modules.ObstacleAvoid import ObstacleAvoid
from modules.UAV import UAV
from modules.Fence import uploadFence
from math import comb

import os
import clr


def startMission(uav: UAV, master, wpPath, obsPath, fencePath, payloadPath, payloadRadius: int = 0) -> None:
    altwp = 70
    wpLoader = mavwp.MAVWPLoader()

    wpCords = ObstacleAvoid(uav, wpPath, obsPath)
    targetCord = readWaypoints(payloadPath)[0]
    lastWp = wpCords[len(wpCords) - 1]
    beforeLastWp = wpCords[len(wpCords) - 2]

    fenceCords = readWaypoints(fencePath)

    uploadFence(master, fencePath)

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)

    # upload normal mission
    for i, cord in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], cord[2]))

    # Upload adjusting Wps

    clr.AddReference(os.path.join(os.getcwd(), "./Algorithms/PathFinder/bin/Release/net8.0/PathFinder.dll"))
    from PathFinder import PayloadPathFinder
    adjustingWps = PayloadPathFinder.FindOptimalPath()

    for i in range(len(adjustingWps) - 1):
        wp = adjustingWps[i]
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            wp[0], wp[1], altwp))

    wp = adjustingWps[len(adjustingWps) - 1]
    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 5, 0, 0,
        wp[0], wp[1], altwp))

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 1, uav.Servo_No, uav.PWM_value, 0, 0,
        0, 0, 0))

    # landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())
    for _ in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))


def addWpAirDrop(payloadCord, d_drop, wpCords, fenceCords, safetyDistance=25, wp_num_to_generate=10):
    lastWp = wpCords[len(wpCords) - 1]
    beforeLastWp = wpCords[len(wpCords) - 2]

    payloadToPlaneBrng = getBearing2Points(payloadCord[0], payloadCord[1], lastWp[0], lastWp[1])
    planeBrng = getBearing2Points(beforeLastWp[0], beforeLastWp[1], lastWp[0], lastWp[1])

    # WHAT TO DO WITH THAT
    bearing_diff = abs((payloadToPlaneBrng+180) - planeBrng)
    bearing_diff = abs(min(360 - bearing_diff, bearing_diff))
    distanceToPayload = getDistance2Points(lastWp[0], lastWp[1], payloadCord[0], payloadCord[1])

    plane_d = 10
    before_drop_d = 10

    plane_d_safe = 200
    before_drop_d_safe = 500

    if distanceToPayload < 50 + d_drop or bearing_diff > 90:
        plane_d = plane_d_safe
        before_drop_d = before_drop_d_safe

    dropBrng = payloadToPlaneBrng
    direction = np.sign((payloadToPlaneBrng - planeBrng + 180) % 360 - 180)

    secWp = new_waypoint(lastWp[0], lastWp[1], plane_d, planeBrng)

    min_distance = float('inf')
    best_dropBrng = None

    while True:
        drop = new_waypoint(payloadCord[0], payloadCord[1], d_drop, dropBrng)
        wpBeforeDrop = new_waypoint(drop[0], drop[1], before_drop_d, dropBrng)

        points = np.array([item[:2] for item in [lastWp, secWp, wpBeforeDrop, drop]])
        curvePnts = bezier_curve(points, 30)
        maxDistanceToFence = max([isPointInFence(point[0], point[1], fenceCords, -safetyDistance) for point in curvePnts])

        if (maxDistanceToFence < min_distance):
            best_dropBrng = dropBrng
            min_distance = maxDistanceToFence

        if (dropBrng > payloadToPlaneBrng + 360 or dropBrng < payloadToPlaneBrng - 360 or min_distance <= 0):
            break

        dropBrng += 1 * direction

    drop = new_waypoint(payloadCord[0], payloadCord[1], d_drop, best_dropBrng)
    wpBeforeDrop = new_waypoint(drop[0], drop[1], before_drop_d, best_dropBrng)

    points = np.array([item[:2] for item in [lastWp, secWp, wpBeforeDrop, drop]])

    return bezier_curve(points, wp_num_to_generate)


def bezier_curve(points, num_points):
    t_values = np.linspace(0, 1, num_points)
    bezier_points = np.zeros((num_points, 2))

    for i, t in enumerate(t_values):
        for j, point in enumerate(points):
            bezier_points[i] += comb(len(points) - 1, j) * (1 - t)**(len(points) - 1 - j) * t**j * point

    return bezier_points


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
