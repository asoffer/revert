from pandac.PandaModules import Point3
from ..lib.physical import Physical
from panda3d.ode import OdeBoxGeom, OdeMass

class Block(Physical):
    def __init__(self, world, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        mass = OdeMass()
        mass.setBox(1000, 2, 2, 2)

        geom = OdeBoxGeom(world.space, 2, 2, 2)

        super(Block, self).__init__(world, mass, geom, "block", loc, False)
