from pandac.PandaModules import Point3
from ..lib.physical import Physical
from panda3d.ode import OdeSphereGeom, OdeMass

class Ball(Physical):
    def __init__(self, game, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        mass = OdeMass()
        mass.setSphere(1000, 1)

        geom = OdeSphereGeom(game.world.space, 1)

        super(Ball, self).__init__(game, mass, geom, "ball", loc, revert = revert)


