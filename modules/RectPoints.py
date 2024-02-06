from typing import List

class RectPoints:
    def __init__(self, topLeft: List[float], topRight: List[float], bottomRight: List[float], bottomLeft: List[float], length):
        self.topLeft = topLeft
        self.topRight = topRight
        self.bottomRight = bottomRight
        self.bottomLeft = bottomLeft
        self.length = length
        self.order()

    def order(self):
        pass
