import cv2
import numpy as np
import time

cap = cv2.VideoCapture(1)

# AI TEAM STOP BEING LAZY
def shouldCapture(frame) -> bool:
    return False

while True:
    ret, frame = cap.read()

    if not ret:
        print("frame not read correctly")
        break

    if shouldCapture(frame):
        ret, frame = cap.read()
        cv2.imwrite('black_frame.png', frame)

    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()