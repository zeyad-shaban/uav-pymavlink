import cv2
import numpy as np
import pytesseract
import json
import time

# Coordinates of the pixel to check for red
pixel_x = 29
pixel_y = 37

# Coordinates of the timestamp region
top_left_x = 40
top_left_y = 25
bottom_right_x = 115
bottom_right_y = 49

# Initialize the JSON data
data = {}

def main():
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    recording_started = False
    last_red_time = None

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Error: Could not read frame or camera unplugged")
                break

            # Get the color of the pixel
            b, g, r = frame[pixel_y, pixel_x]

            # Check if the pixel is red (you might need to adjust the threshold)
            if r > 200 and g < 100 and b < 100:
                if not recording_started:
                    recording_started = True
                    print("Recording started")

                last_red_time = time.time()
                # Extract the timestamp region
                timestamp_region = frame[top_left_y:bottom_right_y, top_left_x:bottom_right_x]
                # Convert to grayscale
                gray = cv2.cvtColor(timestamp_region, cv2.COLOR_BGR2GRAY)
                # Use OCR to extract the timestamp
                timestamp = pytesseract.image_to_string(gray, config='--psm 7').strip()
                # Add to the JSON data
                if timestamp:
                    data[timestamp] = ["lat", "long"]
                    print(f"Timestamp: {timestamp}, Data: {data[timestamp]}")
            else:
                if recording_started and last_red_time and time.time() - last_red_time > 5:
                    print("Red dot not detected for more than 5 seconds. Exiting...")
                    break

            cv2.imshow('Camera Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Script manually stopped")
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Save the JSON data when the script ends
        with open('timestamps.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
