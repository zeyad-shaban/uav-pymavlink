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
import utils

class automission(object):
    # docstring for automission
    def __init__(self, vehicle_type):

        super(automission, self).__init__()
        assert vehicle_type == 'plane'
        self.mlist = []  # each element of the array represents a command, ie waypoint, with its parameters
        self.counter = 1

        # these two lines are by default, exists every mission planner file
        #self.mlist.append(f"QGC WPL 110\n0\t1\t0\t16\t0\t0\t0\t0\t{home_lat}\t{home_long}\t{home_ASL}\t1\n") # Current Home Location

    def param_to_mcommand(self,
                          *args):  # takes command and its parameters, appends them to mlist while adjusting formatting
        string = str(self.counter) + '\t'
        self.counter += 1

        for i in args:
            string += str(i) + '\t'
        string = string.rstrip('\t')
        string += '\n'
        self.mlist.append(string)

    def write(self, name='Waypointsedited'):
        # saves final command list mlist as WP file.
        # Missionplanner can direcly open this text document in flight plan / load WP file button
        # open(str(name)+".waypoints", 'w').close()
        with open(str(name) + ".txt", "w") as text_file:
            for i in self.mlist:
                print(i)
                text_file.write(i)

def download_mission(): #Downloads the current mission and returns it in a list
    #It is used in save_mission() to get the file information to save
    print(" Download mission from vehicle")
    missionlist = []
    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()
    for cmd in cmds:
        missionlist.append(cmd)
    return missionlist

def save_mission(aFileName): #Save a mission in the Waypoint file format
    print("\nSave mission from Vehicle to file: %s" % aFileName)
    missionlist = download_mission() #Download mission from vehicle
    # Add file-format information
    output = 'QGC WPL 110\n'
    home = vehicle.home_location #Add home location as 0th waypoint
    output += "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (0, 1, 0, 16, 0, 0, 0, 0, home.lat, home.lon, home.alt, 1)
    # Add commands
    for cmd in missionlist:
        commandline = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
        cmd.seq, cmd.current, cmd.frame, cmd.command, cmd.param1, cmd.param2, cmd.param3, cmd.param4, cmd.x, cmd.y,
        cmd.z, cmd.autocontinue)
        output += commandline
    with open(aFileName, 'w') as file_:
        print(" Writing mission to file")
        file_.write(output)

def take_off_sequence():
    brng = utils.myUav.main_bearing
    take_off_lat, take_off_long = utils.new_waypoint(home_lat, home_long, 1, brng)
    cmd_takeoff = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, utils.myUav.takeoff_angle, 0, 0, 0, take_off_lat, take_off_long, utils.myUav.takeoff_alt)
    cmds.add(cmd_takeoff)


def landing_sequence(): #Create Landing Sequencex
    brng = utils.myUav.main_bearing  # Bearing Angle in degrees
    start_land_dist = 100
    loiter_alt = 20
    loiter_rad = 50
    loiter_lat,loiter_long = utils.new_waypoint(home_lat,home_long,start_land_dist,brng-180)
    cmd_loiter = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, loiter_rad, 0, 0, loiter_lat, loiter_long, loiter_alt)
    cmd_land = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, home_lat, home_long, 0)
    cmds.add(cmd_loiter)
    cmds.add(cmd_land)

def airdrop_off(waypoints_file,payloads_file):
    #waypoints_file = 'Waypoints'
    #payloads_file = 'Payloads'
    def add_drop_waypoints(LatPL, LongPL, d_drop):
        brng = utils.myUav.main_bearing
        d_wp = 60
        drop_alt = 60
        altwp = 70
        Lat_drop,Long_drop = utils.new_waypoint(LatPL,LongPL,d_drop,brng)
        wpAfter_lat,wpAfter_long = utils.new_waypoint(Lat_drop,Long_drop,d_wp,brng-180)
        wpBefore2_lat,wpBefore2_long = utils.new_waypoint(Lat_drop,Long_drop,d_wp,brng)
        wpBefore1_lat,wpBefore1_long = utils.new_waypoint(Lat_drop,Long_drop,d_wp*2,brng)

        cmdBefore1 = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, wpBefore1_lat, wpBefore1_long, altwp)
        cmdBefore2 = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, wpBefore2_lat, wpBefore2_long, altwp)
        cmd_drop = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, Lat_drop, Long_drop, drop_alt)
        cmd_drop_servo = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 0, utils.myUav.Servo_No, utils.myUav.PWM_value, 0, 0, Lat_drop, Long_drop, drop_alt)
        cmdAfter = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, wpAfter_lat, wpAfter_long, altwp)
        
        cmds.add(cmdBefore1)
        cmds.add(cmdBefore2)
        cmds.add(cmd_drop)
        cmds.add(cmd_drop_servo)
        cmds.add(cmdAfter)

    drop_x, drop_y = utils.payload_drop_eq(utils.myUav.H1, utils.myUav.Vpa, utils.myUav.Vag, utils.myUav.angle)

    WpsList, WpsNo = utils.WP_FileList(waypoints_file)

    file_path = payloads_file + '.csv'
    try:
        with open(file_path) as file:
            print("\nPayloads file available")
            if os.stat(file_path).st_size != 0:
                PL_List, PL_No = utils.FileList(payloads_file)
                for x in range (2):
                    PL_N, PL_Lat, PL_Long = utils.Air_Drop_and_fence_Coordinates(0, PL_List)
                    upload_mission(import_mission_filename)
                    add_drop_waypoints(PL_Lat, PL_Long, drop_x)

    except FileNotFoundError:
        print("\nPayloads file is not available")

    my_mission.write()

utils.csv_Format()
# Upload Geofence
#Fence_Module.uploadfence(robenuav.myUav.fence_file)


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

#upload_mission(import_mission_filename) #Upload mission from file

airdrop_off(waypoints_file,utils.myUav.payloads_file)

landing_sequence()
cmds.upload()  # Send commands

save_mission(export_mission_filename) #Download mission we just uploaded and save to a file

time.sleep(5) #delay 5s

vehicle.close() #Before exiting, clear the vehicle object

utils.printfile(export_mission_filename)
