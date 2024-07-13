import os
import datetime
import time

def seconds_to_date(seconds):
    # Convert seconds since epoch to a datetime object
    date = datetime.datetime.fromtimestamp(seconds)
    return date

def get_creation_time(filename):
    # Get the creation time in seconds since epoch
    creation_time_in_seconds = os.path.getctime(filename)
    return creation_time_in_seconds

# filename = 'D:/DCIM/100GOPRO/GOPR5187.MP4'  # replace with your filename
# creation_time_in_seconds = get_creation_time(filename)
# print(f"The video was created at {creation_time_in_seconds} seconds since the epoch.")

# Get the current time in seconds since the epoch
current_time_in_seconds = time.time()
print(f"The current time is {current_time_in_seconds} seconds since the epoch.")

# # Calculate the time difference in seconds
# time_difference_in_seconds = current_time_in_seconds - creation_time_in_seconds
# print(f"The time difference is {time_difference_in_seconds} seconds.")


# 1.  1720859930.3270013
# 2.  


