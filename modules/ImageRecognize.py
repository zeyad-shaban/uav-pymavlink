from pymavlink import mavutil, mavwp
import cv2
import numpy as np
import time


def start():
    master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("frame not read correctly")
            break

        if np.mean(frame) < 20:
            print("TRUE")
            # Wait for 1 second
            time.sleep(2)

            # Save the image
            ret, frame = cap.read()
            cv2.imwrite('black_frame.png', frame)

    # Release the webcam
    cap.release()