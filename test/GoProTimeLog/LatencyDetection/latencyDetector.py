import cv2
import numpy as np
import time

# Threshold for absolute darkness (all pixel values should be below this threshold to be considered dark)
darkness_threshold = 30

# Define the region of interest (ROI) coordinates
roi_top_left = (7, 77)
roi_bottom_right = (634, 477)

def is_roi_dark(frame, top_left, bottom_right, threshold):
    # Extract the region of interest
    roi = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    # Convert ROI to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Check if all pixel values in the ROI are below the darkness threshold
    return np.all(gray_roi < threshold)

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    print("Cover the camera with a black object and then remove it quickly to measure latency.")
    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame")
            break

        # Check if the ROI is absolutely dark
        if is_roi_dark(frame, roi_top_left, roi_bottom_right, darkness_threshold):
            print("Dark frame detected. Waiting for transition...")

            # Wait until a non-dark frame is detected
            while is_roi_dark(frame, roi_top_left, roi_bottom_right, darkness_threshold):
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not read frame")
                    break

            # Log the timestamp when transition is detected
            print(f"Transition detected at {time.time()}")

        cv2.imshow('Camera Feed', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
