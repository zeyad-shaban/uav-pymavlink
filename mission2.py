from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

msg = master.recv_match(type='COMMAND_ACK' , blocking=True)

