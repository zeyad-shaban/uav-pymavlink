import json


class UAV:
    def __init__(self, path):
        with open(path, 'r') as f:
            data = json.load(f)

        self.main_bearing = data["bearing"]
        self.alt = data["altitude"]
        self.Pa = data["takeOffAngle"]
        self.takeoff_angle = data["takeOffAngle"]
        self.takeoff_alt = data["takeOffAlt"]
        self.safe_dist = data["obsAvoidSafeDistance"]

        # Files
        self.fence_file = data["Files"]["fenceFile"]
        self.waypoints_file = data["Files"]["waypointsFile"]
        self.obstacles_file = data["Files"]["obstaclesFile"]
        self.payloads_file = data["Files"]["payloadsFile"]
        self.grid_file = data["Files"]["searchGridFile"]

        # Airdrop Data H1, Vpa, Vag, angle
        self.H1 = data["airdropData"]["aircraftAltitude"]
        self.Vpa = data["airdropData"]["aircraftVelocity"]
        self.Vag = data["airdropData"]["windSpeed"]
        self.angle = data["airdropData"]["windBearing"]

        self.Servo_No = data["airdropData"]["servoNo"]
        self.PAYLOAD_OPEN_PWM_VALUE = data["airdropData"]["PAYLOAD_OPEN_PWM_VALUE"]
        self.PAYLOAD_CLOSE_PWM_VALUE = data["airdropData"]["PAYLOAD_CLOSE_PWM_VALUE"]
        # self.API = connect(data["connection-string"], wait_ready=True)
        return

    def readmission(self, aFileName):  # Load a mission from a file into a list
        print("\nReading mission from file: %s" % aFileName)
