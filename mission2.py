from pymavlink import mavutil, mavwp

master = mavutil.mavlink_connection("udpin:172.26.240.1:14550")
master.wait_heartbeat()
wpLoader = mavwp.MAVWPLoader()

msg = master.recv_match(type='COMMAND_ACK' , blocking=True)

while True:
    print("thign")
    msg = master.recv_match(type=['MISSION_ITEM', 'MISSION_COUNT'], blocking=True)
    print('yo')
    if msg.get_type() == 'MISSION_COUNT':
        print(f"Received {msg.count} waypoints")
    elif msg.get_type() == 'MISSION_ITEM':
        print(f"Waypoint {msg.seq}: {msg.x}, {msg.y}, {msg.z}")