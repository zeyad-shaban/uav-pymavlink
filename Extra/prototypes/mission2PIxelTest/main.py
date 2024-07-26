# Based on: https://en.wikipedia.org/wiki/Rotation_matrix#Basic_rotations

import numpy as np
import math
from geopy.distance import distance


def getDistance2Points(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km * 1000


class Camera:
    def __init__(self, spacingAt100Alt, focalLength, imgWidth, imgHeight, sensorWidth, sensorHeight):
        self.spacingAt100Alt = spacingAt100Alt
        self.focalLength = focalLength
        self.imgWidth = imgWidth
        self.imgHeight = imgHeight
        self.sensorWidth = sensorWidth
        self.sensorHeight = sensorHeight


sonya6000 = Camera(spacingAt100Alt=47, focalLength=20, imgWidth=6000, imgHeight=4000, sensorWidth=23.5, sensorHeight=15.6)


def pixel_to_geo(lat, lon, alt, yaw, pitch, roll, cam_height, camera, x, y):
    yaw = np.radians(yaw)
    pitch = np.radians(pitch)
    roll = np.radians(roll)

    f_x = (camera.focalLength / camera.sensorWidth) * camera.imgWidth
    f_y = (camera.focalLength / camera.sensorHeight) * camera.imgHeight
    c_x = camera.imgWidth / 2
    c_y = camera.imgHeight / 2

    K = np.array([[f_x, 0, c_x],
                  [0, f_y, c_y],
                  [0, 0, 1]])

    pixel_coords = np.array([x, y, 1])
    norm_coords = np.linalg.inv(K).dot(pixel_coords)

    R_yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                      [np.sin(yaw), np.cos(yaw), 0],
                      [0, 0, 1]])

    R_pitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                        [0, 1, 0],
                        [-np.sin(pitch), 0, np.cos(pitch)]])

    R_roll = np.array([[1, 0, 0],
                       [0, np.cos(roll), -np.sin(roll)],
                       [0, np.sin(roll), np.cos(roll)]])

    R = R_yaw.dot(R_pitch).dot(R_roll)

    camera_position = np.array([lat, lon, cam_height])

    world_coords = R.dot(norm_coords)

    ground_alt = 0

    scale = (ground_alt - alt) / world_coords[2]
    ground_position = camera_position + scale * world_coords

    d = distance(kilometers=np.linalg.norm(ground_position[:2]))
    destination = d.destination((lat, lon), np.degrees(np.arctan2(ground_position[1], ground_position[0])))

    return destination.latitude / 10, destination.longitude / 10


lat, lon = 29.8147596, 30.8248043
alt = 3.01  # meters
yaw, pitch, roll = 0, 0, 0  # degrees
cam_height = alt  # meters
pixel_x, pixel_y = 2713, 1764


latitude, longitude = pixel_to_geo(lat, lon, alt, yaw, pitch, roll, cam_height, sonya6000, pixel_x, pixel_y)
print(f"Geographical coordinates: Latitude = {latitude}, Longitude = {longitude}")


pixel_x2, pixel_y2 = 3121, 1752
latitude2, longitude2 = pixel_to_geo(lat, lon, alt, yaw, pitch, roll, cam_height, sonya6000, pixel_x2, pixel_y2)
print(f"Geographical coordinates: Latitude = {latitude2}, Longitude = {longitude2}")


print(getDistance2Points(latitude, longitude, latitude2, longitude2))