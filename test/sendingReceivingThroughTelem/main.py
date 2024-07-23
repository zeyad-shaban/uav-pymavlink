from pymavlink import mavutil

MISSION_NUMBER = 2

connectionString = "com8:57600"
master = mavutil.mavlink_connection(connectionString)
master.wait_heartbeat()
