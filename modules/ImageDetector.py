import numpy as np


def shouldCapture(frame) -> bool:
    return np.mean(frame) < 20 # will get captured if it gets dark, really dark, AI DO YOUR JOB HERE FR