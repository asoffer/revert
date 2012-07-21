from pandac.PandaModules import Point3, Vec3
from panda3d.bullet import BulletBoxShape

from ..lib.physical import Physical

class Block(Physical):
    def __init__(self, worldNP, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        super(Block, self).__init__(worldNP, "block", loc, revert = revert)

        self.addShape(BulletBoxShape(Vec3(1.5, 1.5, 1.5)))
