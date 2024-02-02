import math
import os
import json
import csv
import robenuav as utils

def obstacle_avoidance(waypoints_file, obstacles_file):
    #waypoints_file = 'Waypoints'
    #obstacles_file = 'Obstacles'
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
            self.param_to_mcommand(0, 3, waypoint_id, delay, 0, 0, 0, lat, lon, alt, 1)

        def takeoff(self, angle, lat, lon, alt):
            takeoff_id = 22
            self.param_to_mcommand(0, 3, takeoff_id, angle, 0, 0, 0, lat, lon, alt, 1)

        def write(self, name='Waypoints+Obstacles'):
            # saves final command list mlist as WP file.
            # Missionplanner can direcly open this text document in flight plan / load WP file button
            # open(str(name)+".waypoints", 'w').close()
            with open(str(name) + ".txt", "w") as text_file:
                for i in self.mlist:
                    print(i)
                    text_file.write(i)

    def check_2nd_time(x1, y1, z1, x2, y2, z2, yy): #
        print("\n")
        for y in range(ObsNo + 1):
            if y != yy:
                ObsLat, ObsLong, ObsRad = utils.Obstacle_Coordinates_Radius(y, ObsList)
                ObsRad = float(ObsRad)
                dAB = utils.distance(x1, y1, x2, y2)  #total distance from A to B
                dAob = utils.distance(x1, y1, ObsLat, ObsLong)  #distance from A to Obstacle
                dobB = utils.distance(ObsLat, ObsLong, x2, y2)  #distance from Obstacle to B
                brngAB = utils.get_bearing(x1, y1, x2, y2)   #bearing between A and B
                brngBA = brngAB - 180   #bearing between B and A
                brngobs = brngAB - 90   #bearing of obs (perpendicular to AB bearing)
                brngAob = utils.get_bearing(x1, y1, ObsLat, ObsLong) #bearing between A and Obstacle
                brngobA = utils.get_bearing(ObsLat, ObsLong, x1, y1)  #bearing between Obstacle and A
                brngobB = utils.get_bearing(ObsLat, ObsLong, x2, y2)  #bearing between Obstacle and B

                if brngAB > brngAob:
                    brng = brngAB - brngAob
                else:
                    brng = brngAob - brngAB

                L = dAob * math.sin(brng*(math.pi/180))

                if (brng <= 270 and brng >= 90 ) or (L >= (utils.myUav.safe_dist * ObsRad)) or (dAob > dAB):
                    print("re Obs",y,"--> No Effect")

                else:
                    print("re Obs",y,"--> Effect")
                    add_avoid_waypoint(x1, y1, z1, x2, y2, z2, ObsLat, ObsLong, ObsRad, brngobs, y)
            else:
                    continue

    def add_avoid_waypoint(LatA, LongA, AltA, LatB, LongB, AltB, ObsLat, ObsLong, ObsRad, brngobs, y):
        dObs = ObsRad * utils.myUav.safe_dist
        d1safe = ObsRad * utils.myUav.safe_dist #Safety Distance
        d2safe = ObsRad * utils.myUav.safe_dist

        '''
        if (d1safe < dAob):
            x1, y1 = robenuav.new_waypoint(ObsLat, ObsLong, d1safe, brngAB-180)
            my_mission.waypoint(x1, y1, AltA)
        else:
            x1 = LatA
            y1 = LongB
        '''

        x2, y2 = utils.new_waypoint(ObsLat, ObsLong, dObs, brngobs)
        #check_2nd_time(x1, y1, AltA, x2, y2, AltA, y)
        check_2nd_time(LatA, LongA, AltA, x2, y2, AltA, y)
        my_mission.waypoint(x2, y2, AltA)
        check_2nd_time(x2, y2, AltA, LatB, LongB, AltB, y)

        '''
        if (d2safe < dobB):
            x3, y3 = robenuav.new_waypoint(ObsLat, ObsLong, d2safe, brngAB)
            check_2nd_time(x2, y2, AltA, x3, y3, AltB, y)
            my_mission.waypoint(x3, y3, AltB)
            '''

    my_mission = automission('plane')
    WpsList, WpsNo = utils.WP_FileList(waypoints_file)

    file_path = obstacles_file + '.csv'
    try:
        with open(file_path) as file:
            print("\nObsatcles file available")
            if os.stat(file_path).st_size == 0:
                for x in range(WpsNo+1):
                    LatA, LongA, AltA = utils.Waypoint_Coordinates_txt(x, WpsList) #get coordinates of first waypoint
                    my_mission.waypoint(LatA, LongA, AltA)
            else:
                ObsListo, ObsNoo = utils.FileList(obstacles_file)
                #Create new obstacle file to add obstacles with close proximity to each other as one
                with open(obstacles_file + 'edited.csv', "a+") as f:
                    f.seek(0) #point at beginning of file
                    f.truncate()
                    f.write("n,lat,long,radius\n")
                    flag = 0
                    for i in range (ObsNoo):
                        if flag == 1:
                            flag = 0 #reintialize the flag to zero after adding past obstacles
                            continue
                        ObsN, ObsLat, ObsLong, ObsRad = utils.Obstacle_Coordinates_Radius(i, ObsListo) #get fist obstacle's lat,long and radius
                        ObsRad = float(ObsRad)

                        ObsN2, ObsLat2, ObsLong2, ObsRad2 = utils.Obstacle_Coordinates_Radius(i+1, ObsListo) #get second obstacle's lat,long and radius
                        ObsRad2 = float(ObsRad2)

                        d_ob1_ob2 = utils.distance(ObsLat, ObsLong, ObsLat2, ObsLong2) #distance between 2 obstacles
                        brng_ob1_ob2 = utils.get_bearing(ObsLat, ObsLong, ObsLat2, ObsLong2) #bearing between 2 obstacles
                        if d_ob1_ob2 <= 30: #if distance is less that 30 m
                            flag = flag + 1 #increment flag to indicate presence of 2 close obstacles
                            m_d_ob1_ob2 = d_ob1_ob2/2  #get midpoint between the radii of the 2 obstacles (to be the new obstacle midpoint)
                            ObsLat_new, ObsLong_new = utils.new_waypoint(ObsLat, ObsLong, m_d_ob1_ob2, brng_ob1_ob2) #add new combined obstacle
                            ObsRad_new = ObsRad + ObsRad2 #new obstacle's radius as sum of both radii
                            #write new obstacle data to new file
                            f.write(str(ObsLat_new))
                            f.write(",")
                            f.write(str(ObsLong_new))
                            f.write(",")
                            f.write(str(ObsRad_new))

                        else:
                            #write existing obstacle data to new file
                            f.write(str(ObsLat))
                            f.write(",")
                            f.write(str(ObsLong))
                            f.write(",")
                            f.write(str(ObsRad))
                        if i < ObsNoo:
                            f.write("\n")

                    #add last obstacle to new obstacle file
                    ObsN, ObsLat, ObsLong, ObsRad = utils.Obstacle_Coordinates_Radius(ObsNoo, ObsListo)
                    ObsRad = float(ObsRad)
                    f.write(str(ObsLat))
                    f.write(",")
                    f.write(str(ObsLong))
                    f.write(",")
                    f.write(str(ObsRad))

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