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

class automission(object):
    pass
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
