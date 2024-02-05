from __future__ import print_function
import time
from dronekit import connect, Command, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil, mavwp
import math
import os
import json
import csv
import Obs_Avoid_Module
import Fence_Module
import modules.utils as utils
# Upload Geofence
Fence_Module.uploadfence(utils.myUav.fence_file)

# Use UDP to connect to the SITL simulator through the local port 14551
connection_string ='127.0.0.1:14551' #'tcp:127.0.0.1:5760'  #
print('Connecting to vehicle on: %s' % connection_string)
# The connect function will return an object of type Vehicle, which is the vehicle here
vehicle = connect(connection_string, wait_ready=True)

my_mission = automission('plane')
wp_file = utils.myUav.waypoints_file + '.csv'
try:
    with open(wp_file) as file:
        print("\nWaypoints file available")
        if os.stat(wp_file).st_size == 0:
            print("No Waypoints in file")
        else:
            WpsList, WpsNo = utils.FileList(utils.myUav.waypoints_file)
            for x in range(WpsNo+1):
                LatA, LongA, AltA = utils.Waypoint_Coordinates(x, WpsList) #get coordinates of first waypoint
                my_mission.waypoint(LatA, LongA, AltA)
            my_mission.write()
    waypoints_file = "Waypointsedited"

except FileNotFoundError:
    print("\nWaypoints file is not available")

cmds = vehicle.commands
cmds.download()
cmds.wait_ready()
cmds.clear()

home = vehicle.home_location #Add home location as 0th waypoint
home_lat = home.lat
home_long = home.lon
home_ASL = home.alt

waypoints_file = Obs_Avoid_Module.obstacle_avoidance(waypoints_file, utils.myUav.obstacles_file)

import_mission_filename = waypoints_file + '.txt'
export_mission_filename = 'Exported_Mission.txt'

take_off_sequence()
cmds.upload()  # Send commands

upload_mission(import_mission_filename) #Upload mission from file

cmd_do_jump = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_JUMP, 0, 0, 2, 6, 0, 0, 0, 0, 0) # repeat 3 laps starting from first Wp (after takeoff point)
cmds.add(cmd_do_jump)

landing_sequence()
cmds.upload()  # Send commands

save_mission(export_mission_filename) #Download mission we just uploaded and save to a file

time.sleep(5) #delay 5s

vehicle.close() #Before exiting, clear the vehicle object

utils.printfile(export_mission_filename)
