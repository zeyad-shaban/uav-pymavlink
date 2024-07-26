import time
from pymavlink import mavutil

connection_string = "udpin:172.31.160.1:14550"
master = mavutil.mavlink_connection(connection_string, baud=57600)

master.wait_heartbeat()

while True:
    msg = master.recv_msg()
    if msg and msg.get_type() == "STATUSTEXT":
        text = msg.text
        print(text)
        # if text.startswith("commandGCS:"):
            # print("Received command:", text)