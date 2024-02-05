import numpy as np
import matplotlib.pyplot as plt


def generate_waypoints(bottom_left, top_right, distance, angle):
    # Convert angle to radians
    angle = np.deg2rad(angle)

    # Create the grid of points
    x = np.arange(bottom_left[0], top_right[0], distance)
    y = np.arange(bottom_left[1], top_right[1], distance)

    # Initialize waypoints list
    waypoints = []

    # Generate waypoints
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            # Rotate the point
            xr = xi * np.cos(angle) - yj * np.sin(angle)
            yr = xi * np.sin(angle) + yj * np.cos(angle)

            # Add the waypoint to the list
            waypoints.append((xr, yr))

        # Reverse the order of y for the next row to create a zigzag pattern
        y = y[::-1]

    return waypoints

def plot_waypoints(waypoints):
    # Unzip the list of waypoints
    x, y = zip(*waypoints)

    # Create the plot
    plt.scatter(x, y)
    plt.show()

# Define the square and grid parameters
bottom_left = (0, 0)
top_right = (10, 10)
distance = 1
angle = 45

# Generate the grid of waypoints
waypoints = generate_waypoints(bottom_left, top_right, distance, angle)

# Plot the waypoints
plot_waypoints(waypoints)
