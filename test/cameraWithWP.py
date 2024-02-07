from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

cord = [29, 30, 80]

wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
    master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 10, 0, 0, 0,
    cord[0], cord[1], cord[2]))

wpLoader.add(mavutil.mavlink.MAVLink_mission_item_message(
    master.target_system, master.target_component, 1, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 10, 0, 0,
    cord[0], cord[1], cord[2]))


master.waypoint_clear_all_send()
master.waypoint_count_send(wpLoader.count())

for i in range(wpLoader.count()):
    msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
    master.mav.send(wpLoader.wp(msg.seq))