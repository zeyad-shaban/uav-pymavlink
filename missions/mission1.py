from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint, readlatlongFile, payload_drop_eq, addHome, takeoffSequence, landingSequence
from modules.ObstacleAvoid import ObstacleAvoid
from modules.Waypoint import Waypoint
# from modules.Fence import uploadFence


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    def airdropOff(payloadPath):
        payloadCords = readlatlongFile(payloadPath)
        brng = uav.main_bearing
        d_wp = 60
        drop_alt = 60
        altwp = 70

        drop_x, drop_y = payload_drop_eq(uav.H1, uav.Vpa, uav.Vag, uav.angle)
        drop_x = 0
        acceptanceRadius = 10

        for payloadCord in payloadCords:
            wpBefore1_lat, wpBefore1_long = new_waypoint(payloadCord[0], payloadCord[1], d_wp*2, brng)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                wpBefore1_lat, wpBefore1_long, altwp
            ))

            wpBefore2_lat, wpBefore2_long = new_waypoint(payloadCord[0], payloadCord[1], d_wp, brng)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, acceptanceRadius, 0, 0,
                wpBefore2_lat, wpBefore2_long, altwp
            ))

            latDrop, longDrop = new_waypoint(payloadCord[0], payloadCord[1], drop_x, brng)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 1, 8, 1500, 0, 0,
                latDrop, longDrop, drop_alt))

            wpAfter_lat, wpAfter_long = new_waypoint(payloadCord[0], payloadCord[1], d_wp, brng-180)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                wpAfter_lat, wpAfter_long, altwp
            ))

            master.waypoint_clear_all_send()
            master.waypoint_count_send(wpLoader.count())

            for i in range(wpLoader.count()):
                msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
                master.mav.send(wpLoader.wp(msg.seq))

    home = addHome(master, wpLoader)
    takeoffSequence(master, wpLoader, home, uav)

    wpCords = ObstacleAvoid(uav, './data/Waypoints.csv', './data/Obstacles.csv')
    for i, cord in enumerate(wpCords):
        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            cord[0], cord[1], cord[2]))

    airdropOff('./data/Payloads.csv')
    landingSequence(master, wpLoader, home, uav)

    master.waypoint_clear_all_send()
    master.waypoint_count_send(wpLoader.count())

    for _ in range(wpLoader.count()):
        msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
        master.mav.send(wpLoader.wp(msg.seq))