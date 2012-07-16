from pandac.PandaModules import Point3
from panda3d.bullet import BulletSphereShape

from ..lib.physical import Physical

class Ball(Physical):
    def __init__(self, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        super(Ball, self).__init__("ball", loc, revert = revert)

        self.addShape(BulletSphereShape(1))


