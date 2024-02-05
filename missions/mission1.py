# TODO implement obstacle avoidance
from pymavlink import mavutil, mavwp
from modules.utils import new_waypoint


def startMission(uav, connectionString):
    master = mavutil.mavlink_connection(connectionString)
    master.wait_heartbeat()
    wpLoader = mavwp.MAVWPLoader()

    def addHome():
        msg = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        home = [msg.lat / 1e7, msg.lon / 1e7]

        mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
            home[0], home[1], 0)

        return home

    def uploadMission():
        master.waypoint_clear_all_send()
        master.waypoint_count_send(wpLoader.count())

        for _ in range(wpLoader.count()):
            msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
            master.mav.send(wpLoader.wp(msg.seq))

    # TODO optimize

    def loadMissionFile(path):
        with open(path) as f:
            lines = f.readlines()

            for i, line in enumerate(lines):
                if i == 0:
                    if not line.startswith("n,lat,long,alt"):
                        return print("File format not supported (must start with n,lat,long,alt)")

                else:
                    line = line.split(",")
                    wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                        master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                        float(line[0]), float(line[1]), float(line[2].strip())
                    ))

    def takeoffSequence(home):
        lat, long = new_waypoint(home[0], home[1], 1, uav.main_bearing)
        wpLoader.insert(1, mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0,
            lat, long, 1
        ))

    def landingSequence(home):
        start_land_dist = 100
        loiter_alt = 20
        loiter_lat, loiter_long = new_waypoint(home[0], home[1], start_land_dist, uav.main_bearing-180)

        wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
            master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0,
            loiter_lat, loiter_long, loiter_alt
        ))

    # TODO send command to servos to throw the payload

    def airdropOff(payloadPath):
        # *What are those?
        payloadCords = []
        with open(payloadPath) as f:
            if not next(f).startswith("n,lat,long"):
                return print("File not supported")

            for line in f:
                line = line.split(',')
                payloadCords.append([float(line[0]), float(line[1])])

        brng = uav.main_bearing
        d_wp = 60
        drop_alt = 60
        altwp = 70

        # TODO enable this
        # drop_x, drop_y = utils.m (utils.myUav.H1, utils.myUav.Vpa, utils.myUav.Vag, utils.myUav.angle)
        drop_x = 0

        for payloadCord in payloadCords:
            wpBefore1_lat, wpBefore1_long = new_waypoint(payloadCord[0], payloadCord[1], d_wp*2, brng)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                wpBefore1_lat, wpBefore1_long, altwp
            ))

            wpBefore2_lat, wpBefore2_long = new_waypoint(payloadCord[0], payloadCord[1], d_wp, brng)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                wpBefore2_lat, wpBefore2_long, altwp
            ))

            # ! THIS DIDN'T WORK IN THE GRAPH SIMULATOR, at least in servoTest.py
            latDrop, longDrop = new_waypoint(payloadCord[0], payloadCord[1], drop_x, brng)
            wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 1, 8, 0, 0, 0,
                latDrop, longDrop, drop_alt
            ))

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

    home = addHome()
    loadMissionFile("./data/Waypoints.csv")
    takeoffSequence(home)
    landingSequence(home)
    airdropOff('./data/Payloads.csv')
    uploadMission()
