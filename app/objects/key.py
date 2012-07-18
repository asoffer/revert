from pandac.PandaModules import Point3
from ..lib.item import Item
from ..lib.pocketable import Pocketable

from panda3d.bullet import BulletSphereShape

class Key(Item, Pocketable):
    def __init__(self, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        super(Key, self).__init__("key", loc, revert)

        #the location here is relative to the objects location
        self.addGhostShape(BulletSphereShape(1.2))

       
