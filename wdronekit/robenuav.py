from __future__ import print_function
import time
from dronekit import connect, Command, VehicleMode, LocationGlobal, LocationGlobalRelative
from pymavlink import mavutil, mavwp
import math
import os
import json
import csv
import numpy as np
import Obs_Avoid_Module
import Fence_Module

R = 6371000.0  #Earth radius in meters

class UAV:
    def __init__(self, data):
        self.main_bearing = data["bearing"]
        self.alt = data["altitude"]
        self.Pa = data["takeOffAngle"]
        self.takeoff_angle = data["takeOffAngle"]
        self.takeoff_alt = data["takeOffAlt"]
        self.safe_dist = data["obsAvoidSafeDistance"]

        #Files
        self.fence_file = data["Files"]["fenceFile"]
        self.waypoints_file = data["Files"]["waypointsFile"]
        self.obstacles_file = data["Files"]["obstaclesFile"]
        self.payloads_file = data["Files"]["payloadsFile"]
        self.grid_file = data["Files"]["searchGridFile"]

        #Airdrop Data H1, Vpa, Vag, angle
        self.H1 = data["airdropData"]["aircraftAltitude"]
        self.Vpa = data["airdropData"]["aircraftVelocity"]
        self.Vag = data["airdropData"]["windSpeed"]
        self.angle = data["airdropData"]["windBearing"]

        self.Servo_No = data["airdropData"]["servoNo"]
        self.PWM_value = data["airdropData"]["PWMValue"]
        #self.API = connect(data["connection-string"], wait_ready=True)
        return

    def readmission(self, aFileName): #Load a mission from a file into a list
        print("\nReading mission from file: %s" % aFileName)
        #cmds = self.API.commands

with open('Data.json','r') as f:
        data = json.load(f)
myUav = UAV(data)

def WP_FileList(filename): #Enumerate lines of waypoint file and add them to a list
    filename = filename + '.txt' #waypoint file as text
    file = open(filename)
    list = []
    for i, line in enumerate(file):
        list.append(line) #adding waypoints to list
    return list, i

def FileList(filename): #Enumerate lines of waypoint file and add them to a list
    filename = filename + '.csv' #waypoint file as csv
    file = open(filename)
    list = []
    for i, line in enumerate(csv.DictReader(file)):
        list.append(line) #adding waypoints to list
    return list, i

def Waypoint_Coordinates_txt(index, listname):
    i = listname[index]
    xlist = i.split() #split waypoint lines to get lat and long
    return xlist[8], xlist[9], xlist[10] #lat[8] long[9] alt[10]

def Waypoint_Coordinates(index, listname):
    i = listname[index]
    if i['alt'] == None:
        i['alt'] = 80
    return i['n'], i['lat'], i['long'], i['alt'] #lat[0] long[1] alt[2]

def Air_Drop_and_fence_Coordinates(index, listname):
    i = listname[index]
    return i['n'], i['lat'], i['long'] #lat[0] long[1]

def Obstacle_Coordinates_Radius(index, listname):
    i = listname[index]
    if i['radius'] == None:
        i['radius'] = 5
    return i['n'], i['lat'], i['long'], i['radius'] #lat[0] long[1] radius[2]

def printfile(aFileName): #Print a mission file to demonstrate "round trip"
    print("\nMission file: %s" % aFileName)
    with open(aFileName) as f:
        for line in f:
            print(' %s' % line.strip())

def Convert(lat, lon): #Convert LAT & LONG from degree to radian
    lat = float(lat) * math.pi / 180
    lon = float(lon) * math.pi / 180
    return lat, lon

# ! THE EQUATION BELOW IS WRONG, 180 / MATH.PI IS NOT COVERED IN BRACKETS
def ReConvert(lat, lon): #Convert LAT & LONG from radian to degree
    lat = float(lat) * 180 / math.pi
    lon = float(lon) * 180 / math.pi
    return lat, lon

def distance(LatA, LongA, LatB, LongB): #Get distance between 2 points
    LatA_r, LongA_r = Convert(LatA, LongA)
    LatB_r, LongB_r = Convert(LatB, LongB)
    LatAB_r = LatB_r - LatA_r
    LongAB_r = LongB_r - LongA_r
    a = ((math.sin(LatAB_r / 2)) * (math.sin(LatAB_r / 2))) + math.cos(LatA_r) * math.cos(LatB_r) * ((math.sin(LongAB_r / 2)) * (math.sin(LongAB_r / 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return (d)

def get_bearing(lat1, long1, lat2, long2): #get bearing between 2 points
    lat1_r, long1_r = Convert(lat1, long1)
    lat2_r, long2_r = Convert(lat2, long2)
    y = math.sin(long2_r - long1_r) * math.cos(lat2_r)
    x = math.cos(lat1_r) * math.sin(lat2_r) - math.sin(lat1_r) * math.cos(lat2_r) * math.cos(long2_r - long1_r)
    i = math.atan2(y, x)
    bearing = (i * 180 / math.pi + 360) % 360
    return bearing

def new_waypoint(lat1, long1, d, brng): #Calculate new waypoint using waypoint, distance and bearing
    brng = brng * (math.pi/180)
    lat1_r, long1_r = Convert(lat1, long1)
    lat2_r = math.asin(math.sin(lat1_r) * math.cos(d / R) + math.cos(lat1_r) * math.sin(d / R) * math.cos(brng))
    long2_r = long1_r + math.atan2((math.sin(brng) * math.sin(d / R) * math.cos(lat1_r)),(math.cos(d / R) - math.sin(lat1_r) * math.sin(lat2_r)))
    lat2, long2 = ReConvert(lat2_r, long2_r)
    brng = brng * (180/math.pi)
    return lat2, long2

def payload_drop_eq (H1, Vpa, Vag, angle):
    g = 9.81 # acceleration due to gravity
    Cd = 0.5 # drag coefficient of payloads
    rho = 1.225 # density of air
    A = 0.02 # average cross section of the payload
    m = 1 # mass of the payload
    H = [float(H1)] #height of the plane in meters
    ty = [0] # duration of fall
    Vy = [0] # velocity in downward direction
    acc = [9.81] # acceleration in downward direction
    Dy = [0] # upward drag force
    dy = [0] # deceleration due to drag force
    k = 1
    int = 0.001 # time intervals for calculation in the loops

    while H[k-1] > 0:
        ty.append(ty[k-1] + int)
        H.append(H[k-1] - (Vy[k-1] * int + 0.5 * acc[k-1] * int**2))
        Vy.append(Vy[k-1] + acc[k-1] * int)
        Dy.append(Cd * rho * (Vy[k-1]**2) * A / 2)
        dy.append(Dy[k-1] / m)
        acc.append(g - dy[k])
        k = k + 1

    print("££££££££££££££££££££££££££££££")
    print("Duration of free-fall:",ty[k-1],"sec")
    print("££££££££££££££££££££££££££££££")

    Vpa = float(Vpa) #cruising velocity in m/s
    Vag = float(Vag) #velocity of wind wrt to ground in m/s
    angle = float(angle) #angle of Vag in degrees

    Vpg = Vpa - Vag * np.cos(np.deg2rad(angle)) # velocity of plane wrt ground
    Vx = [Vpg] # velocity of payload in horizontal direction
    R = [0] # distance covered by payload in horizontal direction
    Dx = [Cd * 1.225 * (Vx[0]**2) * A / 2] # horizontal drag on the payload
    dx = [Dx[0] / m] # horizontal deceleration on the payload
    k = 1

    Vx = np.append(Vx, np.zeros(len(ty)-1))
    R = np.append(R, np.zeros(len(ty)-1))
    Dx = np.append(Dx, np.zeros(len(ty)-1))
    dx = np.append(dx, np.zeros(len(ty)-1))

    for tx in range(len(ty)-1):
        R[k] = R[k-1] + (Vx[k-1] * int - 0.5 * dx[k-1] * int**2)
        Vx[k] = Vx[k-1] - dx[k-1] * int
        Dx[k] = (Cd*1.225*0.5*A) * (Vx[k] ** 2)
        dx[k] = Dx[k] / m
        k = k + 1

    print("££££££££££££££££££££££££££££££")
    print("Range of payload",(R[k-1]),"meter")
    print("££££££££££££££££££££££££££££££")
    x = R[k-1]
    y = H1
    return x, y

def csv_Convert(input_file):
    # Read in the input file
    with open(input_file, 'r') as f_input:
        input_data = f_input.readlines()

    # Replace all spaces with commas in each line
    modified_data = [line.replace(' ', ',') for line in input_data]

    # Write the modified data to the output file
    with open(input_file, 'w') as f_output:
        for line in modified_data:
            f_output.write(line)

def csv_Format():
    csv_Convert(myUav.fence_file + '.csv')
    csv_Convert(myUav.waypoints_file + '.csv')
    csv_Convert(myUav.obstacles_file + '.csv')
    csv_Convert(myUav.payloads_file + '.csv')
