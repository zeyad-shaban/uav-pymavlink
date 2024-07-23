import math


radius = 5
total = 1

lastRadius = radius

for i in range(total):
    distToOrigin = math.sqrt(radius**2 + radius**2)
    distDiff = distToOrigin - lastRadius

    point_x1, point_y1 = distDiff, distDiff
    point_x2, point_y2 = distDiff, 0
    point_x1, point_y1 = 0, distDiff

    newRadius = math.sqrt(0 + distDiff**2)
    print(newRadius)
