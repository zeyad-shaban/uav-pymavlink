from typing import List
import math

def getDistance2Points(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    km = 6371 * c
    return km * 1000

class RectPoints:
    def __init__(self, p1: List[float], p2: List[float], p3: List[float], p4: List[float]):
        cords = [p1, p2, p3, p4]
        sortedByLat = sorted(cords, key=lambda x: x[0])

        print(sortedByLat)

        if sortedByLat[0][1] < sortedByLat[1][1]:
            self.bottomLeft = sortedByLat[0]
            self.bottomRight = sortedByLat[1]
        else:
            self.bottomLeft = sortedByLat[1]
            self.bottomRight = sortedByLat[0]

        if sortedByLat[2][1] < sortedByLat[3][1]:
            self.topLeft = sortedByLat[2]
            self.topRight = sortedByLat[3]
        else:
            self.topLeft = sortedByLat[3]
            self.topRight = sortedByLat[2]

        self.length = getDistance2Points(self.topRight[0], self.topRight[1], self.bottomRight[0], self.bottomRight[1])
        self.width = getDistance2Points(self.topRight[0], self.topRight[1], self.topLeft[0], self.topLeft[1])