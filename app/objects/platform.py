from pandac.PandaModules import Point3, Vec3
from panda3d.bullet import BulletBoxShape

from ..lib.interactable import Interactable

class Platform(Interactable):
    def __init__(self, worldNP, width = 10, rot = 0, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        self.width = width
        super(Platform, self).__init__(worldNP, "platform", loc, False)
        
        self.addShape(BulletBoxShape(Vec3(width / 2, 1.5, 0.2)), rot = rot)

        self.model.setScale(width / 2, 1, 1)
        self.model.setHpr(0, 0, rot)
