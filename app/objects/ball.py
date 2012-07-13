from pandac.PandaModules import Point3
from panda3d.ode import OdeSphereGeom, OdeMass

from ..lib.physical import Physical

import app.world

class Ball(Physical):
    def __init__(self, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        mass = OdeMass()
        mass.setSphere(1000, 1)

        geom = OdeSphereGeom(app.world.WORLD.space, 1)

        super(Ball, self).__init__(mass, geom, "ball", loc, revert = revert)


