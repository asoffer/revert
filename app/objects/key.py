from pandac.PandaModules import Point3
from ..lib.item import Item
from ..lib.pocketable import Pocketable

from panda3d.ode import OdeSphereGeom

import app.world

class Key(Item, Pocketable):
    def __init__(self, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        super(Key, self).__init__("key", loc, revert)

        self.addGeom(OdeSphereGeom(app.world.WORLD.space, 1), loc)


       
