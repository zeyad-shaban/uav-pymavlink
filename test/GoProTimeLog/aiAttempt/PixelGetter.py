import cv2
import numpy as np

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        cv2.imshow('Camera Feed', frame)
        cv2.setMouseCallback('Camera Feed', click_event)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
