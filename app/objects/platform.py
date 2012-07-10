from pandac.PandaModules import Point3
from panda3d.ode import OdeBoxGeom

from ..lib.touchable import Touchable

class Platform(Touchable):
    def __init__(self, world, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        self.width = 20

        super(Platform, self).__init__(world, OdeBoxGeom(world.space, self.width, 0.4, 2), "platform", loc)

        self.model.setScale(self.width/2, 0.2, 1)

