from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()


class Waypoint:
    WAYPIONT_ID: int = mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
    TAKEOFF_ID: int = mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
    LAND_ID: int = mavutil.mavlink.MAV_CMD_NAV_LAND

    def __init__(self, lat: float, lng: float, alt: float, radius: float, id=16):
        self.lat = lat
        self.lng = lng
        self.alt = alt
        self.radius = radius if id == self.waypoint else 0
        self.id = id


wps = [
    Waypoint(29.8157743, 30.8258557, 0,  0),
    Waypoint(29.8168169, 30.8259630, 20, 0, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF),
    Waypoint(29.8218992, 30.8264565, 80, 200),
    Waypoint(29.8219737, 30.8355331, 80, 200),
    Waypoint(29.8163328, 30.8348250, 80, 200),
    Waypoint(29.8168169, 30.8264995, 0,  0, mavutil.mavlink.MAV_CMD_NAV_LAND),
]

for i, cord in enumerate(wps):
    wp = mavutil.mavlink.MAVLink_mission_item_message(
        master.target_system, master.target_component, i, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, cord.id, 0, 1, 0, cord.radius, 0, 0,
        cord.lat, cord.lng, cord.alt)
    wpLoader.add(wp)

master.waypoint_clear_all_send()
master.waypoint_count_send(wpLoader.count())

for i in range(wpLoader.count()):
    msg = master.recv_match(type='MISSION_REQUEST', blocking=True)
    master.mav.send(wpLoader.wp(msg.seq))


master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mavutil.mavlink.PLANE_MODE_AUTO
)
master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
