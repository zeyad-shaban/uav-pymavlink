from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint, readWaypoints, addHome, takeoffSequence, landingSequence, getBearing2Points, isPointInFence, getDistance2Points
from modules.ObstacleAvoid import ObstacleAvoid
from modules.UAV import UAV
from modules.Fence import uploadFence
from modules.PythonNetTypeBridge import asNetArray, asNumpyArray
from math import comb

import numpy as np
import os
import clr


def startMission(uav: UAV, master, wpPath, obsPath, fencePath, payloadPath, payloadRadius: int = 0) -> None:
    MAX_EXECUTE_TIME = 10  # second

    clr.AddReference(os.path.join(os.getcwd(), "Algorithms\PathFinder\\PathFinder\\bin\\Release\\PathFinder.dll"))
    from PathFinder.Fundamentals import PayloadPathFinder

    wpLoader = mavwp.MAVWPLoader()

    wpCords = ObstacleAvoid(uav, wpPath, obsPath)
    obsCords = [] if obsPath is None else readWaypoints(obsPath)

    targetCord = readWaypoints(payloadPath)[0]
    lastWp = wpCords[len(wpCords) - 1]
    beforeLastWp = wpCords[len(wpCords) - 2]

    fenceCords = readWaypoints(fencePath)

    uploadFence(master, fencePath)

    home = addHome(master, wpLoader, uav)
    takeoffSequence(master, wpLoader, home, uav)

    # upload normal mission
    for i, cord in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], uav.alt))

    # Upload adjusting Wps
    print(f"PID: {os.getpid()}")

    adjustingWps = asNumpyArray(PayloadPathFinder.FindOptimalPath(
        asNetArray(np.array(obsCords) if len(obsCords) > 0 else np.empty((0, 2))),
        asNetArray(np.array(beforeLastWp)),
        asNetArray(np.array(lastWp)),
        asNetArray(np.array(targetCord)),
        asNetArray(np.array(fenceCords)),
        MAX_EXECUTE_TIME,
        float(uav.H1),
        float(uav.Vpa),
        float(uav.Vag),
        float(uav.angle)
    ))

    for i in range(len(adjustingWps) - 1):
        wp = adjustingWps[i]
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            wp[0], wp[1], uav.alt))

    lastAdjustingWp = adjustingWps[-1]
    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, uav.PAYLOAD_ACCEPTANCE_RADIUS, 0, 0,
        lastAdjustingWp[0], lastAdjustingWp[1], uav.alt))

    # Servo control
    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 1, uav.Servo_No, uav.PAYLOAD_OPEN_PWM_VALUE, 0, 0,
        0, 0, 0))

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
        targetCord[0], targetCord[1], uav.alt))

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 1, uav.Servo_No, uav.PAYLOAD_CLOSE_PWM_VALUE, 0, 0,
        0, 0, 0))

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())
    for _ in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))
