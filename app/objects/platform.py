from pandac.PandaModules import Point3, Vec3, Mat3, Quat

from ..lib.interactable import Interactable

class Platform(Interactable):
    def __init__(self, width = 10, rot = 0, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        self.width = width
        super(Platform, self).__init__("platform", loc, False)
        #self.model.setScale(width, 1, 1)
 
