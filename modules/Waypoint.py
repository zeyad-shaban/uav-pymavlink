from pymavlink import mavutil

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