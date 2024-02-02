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

    ### Mission Commands ###
    # every parameter list begins with '0,3,' and ends with ',1'

    def waypoint(self, lat, lon, alt, delay=0):
        waypoint_id = 16
        self.param_to_mcommand(0, 3, waypoint_id, delay, 0, 0, 0, lat, lon, alt,1)

    def takeoff(self, angle, lat, lon, alt):
        takeoff_id = 22
        self.param_to_mcommand(0, 3, takeoff_id, angle, 0, 0, 0, lat, lon, alt,1)

    def write(self, name='Waypointsedited'):
        # saves final command list mlist as WP file.
        # Missionplanner can direcly open this text document in flight plan / load WP file button
        # open(str(name)+".waypoints", 'w').close()
        with open(str(name) + ".txt", "w") as text_file:
            for i in self.mlist:
                print(i)
                text_file.write(i)

def readmission(aFileName): #Load a mission from a file into a list
    print("\nReading mission from file: %s" % aFileName)
    cmds = vehicle.commands
    missionlist = []
    with open(aFileName) as f:
        for i, line in enumerate(f):
            linearray = line.split('\t')
            ln_index = int(linearray[0])
            ln_currentwp = int(linearray[1])
            ln_frame = int(linearray[2])
            ln_command = int(linearray[3])
            ln_param1 = float(linearray[4])
            ln_param2 = float(linearray[5])
            ln_param3 = float(linearray[6])
            ln_param4 = float(linearray[7])
            ln_param5 = float(linearray[8])
            ln_param6 = float(linearray[9])
            ln_param7 = float(linearray[10])
            ln_autocontinue = int(linearray[11].strip())
            cmd = Command(0, 0, 0, ln_frame, ln_command, ln_currentwp, ln_autocontinue, ln_param1, ln_param2,
                          ln_param3, ln_param4, ln_param5, ln_param6, ln_param7)
            missionlist.append(cmd)
    return missionlist

def upload_mission(aFileName): #Upload a mission from a file
    missionlist = readmission(aFileName) # Read mission from file
    print("\nUpload mission from a file: %s" % aFileName)
    print(' Clear mission')
    cmds = vehicle.commands
    #cmds.clear() # Clear existing mission from vehicle
    # Add new mission to vehicle
    for command in missionlist:
        cmds.add(command)
    print(' Upload mission')
    vehicle.commands.upload()

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


def landing_sequence(): #Create Landing Sequence
    brng = utils.myUav.main_bearing  # Bearing Angle in degrees
    start_land_dist = 100
    loiter_alt = 20
    loiter_rad = 50
    loiter_lat,loiter_long = utils.new_waypoint(home_lat,home_long,start_land_dist,brng-180)
    cmd_loiter = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LOITER_TO_ALT, 0, 0, 0, loiter_rad, 0, 0, loiter_lat, loiter_long, loiter_alt)
    cmd_land = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, home_lat, home_long, 0)
    cmds.add(cmd_loiter)
    cmds.add(cmd_land)

def add_survey(waypoints_filename,grid_filename):
    # Determine the last line number in the output file
    with open(waypoints_filename + "2.txt", "a+") as wp_grid_file:
        wp_grid_file.seek(0)
        wp_grid_file.truncate()
        with open(grid_filename + ".txt", "r") as grid_file:
            # Skip the first two lines
            next(grid_file)
            next(grid_file)
            # Read the remaining lines
            lines_grid = grid_file.readlines()

        with open(waypoints_filename + ".txt", "r") as wp_file:
            # Write the lines to the output file
            lines_wp = wp_file.readlines()

        # Write the lines to the output file with line numbers
        wp_grid_file.writelines(lines_wp)
        wp_grid_file.writelines(lines_grid)

    with open(waypoints_filename + "2.txt", "r+") as wp_grid_file:
        wp_grid_lines = wp_grid_file.readlines()
        # Initialize a counter for the new numbers
        counter = 0

        # Loop through each line in the file
        for i in range(len(wp_grid_lines)):
            # Split the line by whitespace
            items = wp_grid_lines[i].split()
            # Replace the first item with the counter value
            items[0] = str(counter)
            # Join the items back into a line
            wp_grid_lines[i] = "\t".join(items) + "\n"
            # Increment the counter
            counter += 1

        # Open the file in write mode
        with open(waypoints_filename + "2.txt", "w") as f:
            # Write all the modified lines to the file
            f.writelines(wp_grid_lines)
        return waypoints_filename + "2"

def airdrop_off(waypoints_file,payloads_file):
    #waypoints_file = 'Waypoints'
    #payloads_file = 'Payloads'
    def add_drop_waypoints(LatPL, LongPL, d_drop):
        brng = vehicle.heading-180
        d_wp = 60
        drop_alt = 60
        altwp = 70
        Lat_drop,Long_drop = utils.new_waypoint(LatPL,LongPL,d_drop,brng)
        wp2_lat,wp2_long = utils.new_waypoint(Lat_drop,Long_drop,d_wp,brng-180)
        wp1_lat,wp1_long = utils.new_waypoint(Lat_drop,Long_drop,d_wp,brng)

        cmd1 = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, wp1_lat, wp1_long, altwp)
        cmd_drop = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, Lat_drop, Long_drop, drop_alt)
        cmd_drop_servo = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_DO_SET_SERVO, 0, 0, utils.myUav.Servo_No, utils.myUav.PWM_value, 0, 0, Lat_drop, Long_drop, drop_alt)
        cmd2 = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, wp2_lat, wp2_long, altwp)

        cmds.add(cmd1)
        cmds.add(cmd_drop)
        cmds.add(cmd_drop_servo)
        cmds.add(cmd2)

    drop_x, drop_y = utils.payload_drop_eq (utils.myUav.H1, utils.myUav.Vpa, utils.myUav.Vag, utils.myUav.angle)

    WpsList, WpsNo = utils.WP_FileList(waypoints_file)

    file_path = payloads_file + '.csv'
    try:
        with open(file_path) as file:
            print("\nPayloads file available")
            if os.stat(file_path).st_size != 0:
                PL_List, PL_No = utils.FileList(payloads_file)
                for x in range (PL_No + 1):
                    PL_Lat, PL_Long = utils.Air_Drop_and_fence_Coordinates(x, PL_List)
                    add_drop_waypoints(PL_Lat, PL_Long, drop_x)


    except FileNotFoundError:
        print("\nPayloads file is not available")

    my_mission.write()

def image_coordinates():
    pixelFile = "Pixels"
    p2List, p2No = utils.FileList(pixelFile)
    with open("Geoloc.txt",'a') as f:
        f.seek(0)
        for x in range(p2No+1):
            p2 = p2List[x]
            p2_width = p2['x']
            p2_length = p2['y']
            #p2 = [279,272] # random point from AI'S code

            h_plane = float(vehicle.location.global_frame.alt) #h_plane=80 #altitude of plane
            #h_plane = 80
            w_sensor = 6.17 #width sensor
            l_sensor = 4.55 #length sensor
            fl = 2.92 #focal length

            #Current Locaation
            lat1 = float(vehicle.location.global_frame.lat)
            long1 = float(vehicle.location.global_frame.lon)

            #lat1 = 29.8259667414763
            #long1 = 31.3282012939453

            #pixels in image
            p1 = [2000,1500] #center of image

            pixels_width = abs(float(p1[0]) - float(p2_width))
            pixels_length = abs(float(p1[1]) - float(p2_length))

            gsdw = float((h_plane*w_sensor) / (fl*4000))
            gsdl = float((h_plane*l_sensor) / (fl*3000))
            land_width = gsdw*pixels_width
            land_length = gsdl*pixels_length
            #landwidth = gsdw*1920
            #landlength = gsdl*1080
            distance = math.sqrt( ((land_width)**2) + ((land_length)**2) ) #distance in meters

            d1= p1[0] - int(p2_width)
            d2 = p1[1] - int(p2_length)

            if d1 >= 0 and d2 >= 0 : #First quad
                angle = math.degrees(math.atan(d1/d2))

            elif d1 <= 0 and d2 >= 0 : #second quad
                d2=-d2
                angle = 360 - math.degrees(math.atan(d1/d2))

            elif d1 <= 0 and d2 <= 0: #Third quad
                angle = 270 - math.degrees(math.atan(d2/d1))

            else:
                d2=-d2
                angle = 180 - math.degrees(math.atan(d1/d2))

            #bearing = vehicle.heading #Current bearing
            bearing = 0
            Angle = bearing - angle

            image_x2, image_y2 = utils.new_waypoint(lat1, long1, distance, Angle)

            f.truncate()
            f.write(str(image_x2))
            f.write(",")
            f.write(str(image_y2))
            f.write("\n")

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

waypoints_file = add_survey(waypoints_file,utils.myUav.grid_file)

import_mission_filename = waypoints_file + '.txt'
export_mission_filename = 'Exported_Mission.txt'

take_off_sequence()
cmds.upload()  # Send commands

upload_mission(import_mission_filename) #Upload mission from file

image_coordinates()

airdrop_off(waypoints_file,utils.myUav.payloads_file)

landing_sequence()
cmds.upload()  # Send commands

save_mission(export_mission_filename) #Download mission we just uploaded and save to a file

time.sleep(5) #delay 5s

vehicle.close() #Before exiting, clear the vehicle object

utils.printfile(export_mission_filename)
