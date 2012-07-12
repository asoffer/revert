from pandac.PandaModules import Point3
from ..lib.physical import Physical
from panda3d.ode import OdeBoxGeom, OdeMass

class Block(Physical):
    def __init__(self, world, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        mass = OdeMass()
        mass.setBox(500, 3, 3, 3)

        geom = OdeBoxGeom(world.space, 3, 3, 3)

        super(Block, self).__init__(world, mass, geom, "block", loc)
