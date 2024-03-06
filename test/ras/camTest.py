import cv2
import time
import numpy as np

lastIndex = 0
cap = cv2.VideoCapture(1)
while True:
    ret, frame = cap.read()
    if not ret:
        print("!!!!!FRAME NOT READ CORRECTLY!!!!!")
        break

    cv2.imshow("Yo", frame)

    if np.mean(frame) < 20:
        time.sleep(0.5)
        cv2.imwrite(f'./test.png', cap.read()[1])
        lastIndex += 1
        time.sleep(0.5)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()