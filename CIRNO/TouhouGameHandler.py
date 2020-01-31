import numpy as np

# The Touhou Project POI Processors

class THGame():
    scale = 1

    def __init__(self, scale):
        self.scale = scale

    def PointOfInterestProcess(self, img):
        pass


class THGameKouma(THGame):
    PreDefinedPOI = (37, 477, 40, 418)

    def __init__(self, scale):
        super().__init__(scale)

    def PointOfInterestProcess(self, img):

        # pylint: disable=unsubscriptable-object
        poi_game = np.float32(img)[
            int(self.PreDefinedPOI[0] * self.scale):int(self.PreDefinedPOI[1] * self.scale),
            int(self.PreDefinedPOI[2] * self.scale):int((self.PreDefinedPOI[3] * self.scale))]
        return poi_game


class THGameRensen(THGame):
    PreDefinedPOI = (37, 477, 40, 418)

    def __init__(self, scale):
        super().__init__(scale)

    def PointOfInterestProcess(self, img):

        # pylint: disable=unsubscriptable-object
        poi_game = np.float32(img)[
            int(self.PreDefinedPOI[0] * self.scale):int(self.PreDefinedPOI[1] * self.scale),
            int(self.PreDefinedPOI[2] * self.scale):int((self.PreDefinedPOI[3] * self.scale))]
        return poi_game
