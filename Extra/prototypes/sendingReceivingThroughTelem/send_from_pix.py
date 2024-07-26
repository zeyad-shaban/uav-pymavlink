from pymavlink import mavutil

# Define the connection string for sending
master = mavutil.mavlink_connection('COM4', baud=57600)

# Wait for the first heartbeat to ensure connection
master.wait_heartbeat()
print("Heartbeat received from system (system %u component %u)" % (master.target_system, master.target_component))

# Define the severity level (0-255, lower is more critical)
severity = mavutil.mavlink.MAV_SEVERITY_INFO  # For example, 6 (info level)

# Define the custom message
custom_message = "hello world"

# Send the STATUSTEXT message
master.mav.statustext_send(severity, custom_message.encode('utf-8'))

print("Custom message sent")