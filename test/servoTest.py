from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

wphome = mavutil.mavlink.MAVLink_mission_item_message(
    master.target_system, master.target_component, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
    29.8140615, 30.8258343, 0
)


wpTakeoff = mavutil.mavlink.MAVLink_mission_item_message(
    master.target_system, master.target_component, 1, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 1, 0, 0, 0, 0,
    29.8157557 + 0.01, 30.8265209 + 0.01, 20
)

wpMid = mavutil.mavlink.MAVLink_mission_item_message(master.target_system, master.target_component, 2, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 1, 0, 0, 0, 0,
                                                     29.8157557 + 0.05, 30.8265209 + 0.05, 100
                                                     )

servo_command = mavutil.mavlink.MAVLink_mission_item_message(
    master.target_system,  # target system
    master.target_component,  # target component
    2,  # sequence number (same as the mid-flight waypoint)
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,  # frame
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO,  # command
    0,  # current
    1,  # autocontinue
    8,  # servo number
    1500,  # PWM value
    0, 0, 0,  # parameters 1-3
    wpMid.x, wpMid.y, wpMid.z
)

wpLand = mavutil.mavlink.MAVLink_mission_item_message(
    master.target_system, master.target_component, 3, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 1, 0, 0, 0, 0,
    29.8157557 + 0.1, 30.8265209 + 0.1, 0
)

# add waypoints
wpLoader.add(wphome)
wpLoader.add(wpTakeoff)
wpLoader.add(wpMid)
wpLoader.add(servo_command)
wpLoader.add(wpLand)

master.waypoint_clear_all_send()
master.waypoint_count_send(wpLoader.count())

for i in range(wpLoader.count()):
    msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
    master.mav.send(wpLoader.wp(msg.seq))

master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0,0,0,0,0)
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mavutil.mavlink.PLANE_MODE_AUTO
)

while True:
    msg = master.recv_match(type='MISSION_CURRENT' , blocking=True)
    print(msg.seq)