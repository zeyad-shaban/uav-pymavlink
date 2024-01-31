from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:localhost:14551")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

def uploadMissionFile(path):
    with open(path) as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            if i == 0:
                if not line.startswith("n,lat,long,alt"):
                    return print("File format not supported (must start with n,lat,long,alt)")

            else:
                line = line.split(",")
                cmd = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
                if i == 2:
                    cmd = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
                elif i == len(lines) - 1:
                    cmd = mavutil.mavlink.MAV_CMD_NAV_LAND
                else:
                    cmd = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT

                wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
                    master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, cmd, 0, 1, 0, 0, 0, 0,
                    float(line[0]), float(line[1]), float(line[2].strip())
                ))

        master.waypoint_clear_all_send()
        master.waypoint_count_send(wpLoader.count())

        for i in range(wpLoader.count()):
            msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
            master.mav.send(wpLoader.wp(msg.seq))

uploadMissionFile("Waypoints.csv")
