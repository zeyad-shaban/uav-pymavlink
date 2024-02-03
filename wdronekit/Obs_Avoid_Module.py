import math
import os
import json
import csv
import robenuav as utils

def obstacle_avoidance(waypoints_file, obstacles_file):
    try:
        with open(file_path) as file:
            if False:
                pass
            else:
                ObsListo, ObsNoo = utils.FileList(obstacles_file)
                #Create new obstacle file to add obstacles with close proximity to each other as one
                ObsList, ObsNo = utils.FileList(obstacles_file + 'edited')

                for x in range(WpsNo):
                    print("\n")
                    print("Between Wp",x,"and Wp",x+1)
                    LatA, LongA, AltA = utils.Waypoint_Coordinates_txt(x, WpsList) #get coordinates of first waypoint
                    LatB, LongB, AltB = utils.Waypoint_Coordinates_txt(x+1, WpsList) #get coordinates of first waypoint

                    my_mission.waypoint(LatA, LongA, AltA)
                    for y in range(ObsNo + 1):
                        ObsN, ObsLat, ObsLong, ObsRad = utils.Obstacle_Coordinates_Radius(y, ObsList) #get obstacle's lat,long and radius
                        ObsRad = float(ObsRad)
                        dAB = utils.distance(LatA, LongA, LatB, LongB)  #total distance from A to B
                        dAob = utils.distance(LatA, LongA, ObsLat, ObsLong)  #distance from A to Obstacle
                        dobB = utils.distance(ObsLat, ObsLong, LatB, LongB)  #distance from Obstacle to B
                        brngAB = utils.get_bearing(LatA, LongA, LatB, LongB) #bearing between A and B
                        brngBA = brngAB - 180 #bearing between B and A
                        brngobs = brngAB - 90 #bearing of obs (perpendicular to AB bearing)
                        brngAob = utils.get_bearing(LatA, LongA, ObsLat, ObsLong) #bearing between A and Obstacle
                        brngobA = utils.get_bearing(ObsLat, ObsLong, LatA, LongA) #bearing between Obstacle and A
                        brngobB = utils.get_bearing(ObsLat, ObsLong, LatB, LongB) #bearing between Obstacle and B

                        if brngAB > brngAob:
                            brng = brngAB - brngAob
                        else:
                            brng = brngAob - brngAB

                        L = dAob * math.sin(brng*(math.pi/180))

                        if (brng <= 270 and brng >= 90 ) or (L >= (utils.myUav.safe_dist * ObsRad)) or (dAob > dAB):
                            print("Obs",y,"--> No Effect")

                        else:
                            print("Obs",y,"--> Effect")
                            add_avoid_waypoint(LatA, LongA, AltA, LatB, LongB, AltB, ObsLat, ObsLong, ObsRad, brngobs, y)

                my_mission.waypoint(LatB, LongB, AltB) #add last waypoint to output file
    except FileNotFoundError:
        print("\nObstacles file is not available")
        for x in range(WpsNo+1):
            LatA, LongA, AltA = utils.Waypoint_Coordinates_txt(x, WpsList) #get coordinates of first waypoint
            my_mission.waypoint(LatA, LongA, AltA)
    my_mission.write()
    return 'Waypoints+Obstacles'