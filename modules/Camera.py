class Camera():
    def __init__(self, spacingAt100Alt: float, focalLength: float, imgWidth: float, imgHeight: float, sensorWidth: float, sensorHeight: float):
        self.spacing = spacingAt100Alt
        self.focalLength = focalLength
        self.imgWidth = imgWidth
        self.imgHeight = imgHeight
        self.sensorWidth = sensorWidth
        self.sensorHeight = sensorHeight
    
    def adjutSpacingToAlt(self, alt: float):
        self.spacing *= alt / 100