import numpy as np
import psutil
from PIL import Image
from Utils.OSHandler import isWindows

# The Touhou Project POI Processors

class THGamePOI():
    scale = 1

    def __init__(self, scale):
        self.scale = scale

    def PointOfInterestProcess(self, img):
        pass

    def getViewportWidth(self):
        pass

    def getViewportHeight(self):
        pass


class THGamePOIKouma(THGamePOI):
    preDefinedPOIUpperLeft = (40, 37)
    preDefinedPOIBelowRight = (418, 477)
    # 40, 37
    # 418, 477

    def __init__(self, scale):
        super().__init__(scale)

    def PointOfInterestProcess(self, img):

        # pylint: disable=unsubscriptable-object
        poi_game = img.crop(
            (
                int(self.PreDefinedPOIUpperLeft[0] * self.scale),
                int(self.PreDefinedPOIUpperLeft[1] * self.scale),
                int(self.PreDefinedPOIBelowRight[0] * self.scale),
                int(self.PreDefinedPOIBelowRight[1] * self.scale)
            )
        ).resize((self.getViewportWidth(), self.getViewportHeight()))

        return poi_game

    def getViewportWidth(self):
        return self.preDefinedPOIBelowRight[0] - self.preDefinedPOIUpperLeft[0]

    def getViewportHeight(self):
        return self.preDefinedPOIBelowRight[1] - self.preDefinedPOIUpperLeft[1]

class THGamePOIRensen(THGamePOI):
    preDefinedPOIUpperLeft = (40, 37)
    preDefinedPOIBelowRight = (418, 477)
    # 40, 37
    # 418, 477

    def __init__(self, scale):
        super().__init__(scale)

    def PointOfInterestProcess(self, img):

        # pylint: disable=unsubscriptable-object
        poi_game = img.crop(
            (
                int(self.PreDefinedPOIUpperLeft[0] * self.scale),
                int(self.PreDefinedPOIUpperLeft[1] * self.scale),
                int(self.PreDefinedPOIBelowRight[0] * self.scale),
                int(self.PreDefinedPOIBelowRight[1] * self.scale)
            )
        ).resize((self.getViewportWidth(), self.getViewportHeight()))

        return poi_game

    def getViewportWidth(self):
        return self.preDefinedPOIBelowRight[0] - self.preDefinedPOIUpperLeft[0]

    def getViewportHeight(self):
        return self.preDefinedPOIBelowRight[1] - self.preDefinedPOIUpperLeft[1]

