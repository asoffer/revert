from pandac.PandaModules import Point3, Vec3, Mat3, Quat
from panda3d.ode import OdeBoxGeom

from ..lib.touchable import Touchable
import app.world as World

class Platform(Touchable):
    def __init__(self, width = 10, rot = 0, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        self.width = width
        geom = OdeBoxGeom(World.getSpace(), self.width, 0.2, 1)
        geom.setRotation(Mat3.rotateMatNormaxis(rot, Vec3(0,0,1)))
        super(Platform, self).__init__(geom, "platform", loc, False)

        self.model.setQuat(Quat(geom.getQuaternion()))
        self.model.setScale(self.width/2, 1, 1)

