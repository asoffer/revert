from pandac.PandaModules import Point3
from panda3d.ode import OdeBoxGeom, OdeMass

from ..lib.physical import Physical

import app.world

class Block(Physical):
    def __init__(self, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        mass = OdeMass()
        mass.setBox(500, 3, 3, 3)

        geom = OdeBoxGeom(app.world.WORLD.space, 3, 3, 3)

        super(Block, self).__init__(mass, geom, "block", loc, revert = revert)
