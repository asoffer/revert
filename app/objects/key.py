from pandac.PandaModules import Point3
from ..lib.pocketable import Pocketable

from panda3d.bullet import BulletSphereShape

class Key(Pocketable):
    def __init__(self, worldNP, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        super(Key, self).__init__(worldNP, "key", loc = loc, revert = revert)

        #the location here is relative to the objects location
        self.addGhostShape(BulletSphereShape(1.2))

       
