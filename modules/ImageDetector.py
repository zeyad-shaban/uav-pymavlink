import numpy as np
from typing import List

def openCam():
    print("opening cam")

def closeCam():
    print("closing cam")

def capturePixels(frame):
    if np.mean(frame) < 20:
        # AI DO YOUR JOB HERE AND FOR THE CONDITION OFC
        # * saving files is handeled in mission2.py itself, no need to worry about it
        x = 10
        y = 20
        return [x, y]
