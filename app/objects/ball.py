from pandac.PandaModules import Point3
from ..lib.physical import Physical
from panda3d.ode import OdeSphereGeom, OdeMass

class Ball(Physical):
    def __init__(self, world, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        mass = OdeMass()
        mass.setSphere(1000, 1)

        geom = OdeSphereGeom(world.space, 1)

        super(Ball, self).__init__(world, mass, geom, "ball", loc)


