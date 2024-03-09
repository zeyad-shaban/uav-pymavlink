# TODO LOITER LAND
from pymavlink import mavutil, mavwp
from modules.utils import addHome, takeoffSequence, landingSequence
from modules.ObstacleAvoid import ObstacleAvoid
from modules.Fence import uploadFence


def startMission(uav, master, wpPath, obsPath, fencePath):
    wpLoader = mavwp.MAVWPLoader()
    uploadFence(master, fencePath)

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)
    wpCords = ObstacleAvoid(uav, wpPath, obsPath)
    for i, cord in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], cord[2]))

    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, i + 1, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_JUMP, 0, 1,
        1, 3, 0, 0, 0, 0, 0)
    )

    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for i in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))
