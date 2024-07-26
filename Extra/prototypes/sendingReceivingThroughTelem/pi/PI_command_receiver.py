import os
from pymavlink import mavutil
import subprocess

curr_dir = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.join(curr_dir, "sony_sender.py")

process = None

connection_string = "udpin:172.31.160.1:14550"
master = mavutil.mavlink_connection(connection_string, baud=57600)

master.wait_heartbeat()

while True:
    msg = master.recv_msg()
    if msg and msg.get_type() == "STATUSTEXT":
        text = msg.text
        text = text.lower()

        if text.startswith("command"):
            if "start" in text:
                process = subprocess.Popen(["python", script_path])
                input("kill me")

            elif "stop" in text or "Kill" in text:
                if process:
                    process.kill()

            elif "restart" in text:
                if process:
                    process.kill()
                process = subprocess.Popen(["python", script_path])