from pandac.PandaModules import Point3, BitMask32, Quat
from panda3d.ode import OdeWorld, OdeBody, OdeMass, OdeBoxGeom

from .touchable import Touchable

class Physical(Touchable):
    """ 
    The Physical class is the base class for anything that responds to physics
    """

    def __init__(self, world, mass, geom, model, loc = Point3(), rot = True):
        super(Physical, self).__init__(world, geom, model, loc)

        self.toRevert['rot'] = self.setRot
        self.toSave['rot'] = self.getRot

        self.toRevert['vel'] = self.setVel
        self.toSave['vel'] = self.getVel
        self.toRevert['angVel'] = self.setAngVel
        self.toSave['angVel'] = self.getAngVel

        self.setRevertable(True)

        self.body = OdeBody(world.world)
        self.mass = mass
        self.body.setMass(self.mass)

        self.body.setPosition(self.model.getPos())
        self.body.setQuaternion(self.model.getQuat())

        self.geom.setBody(self.body)

        self.rot = rot

    def constrainPosQuat(self):
        """keep the object rotating in the correct plane"""

        #FIXME is there a better way than fixing at every instant?
        self.body.setPosition(self.body.getPosition()[0], self.body.getPosition()[1], 0)

        if not self.rot:
            self.body.setQuaternion(Quat.identQuat())
            return

        q = self.body.getQuaternion()
        q[1] = 0
        q[2] = 0
        q.normalize()
        self.body.setQuaternion(Quat(q))

    def getPos(self):
        return self.body.getPosition()

    def setPos(self, pos):
        return self.body.setPosition(pos)

    def setRot(self, rot):
        self.body.setQuaternion(Quat(rot))

    def getRot(self):
        return self.body.getQuaternion()

    def setVel(self, vel):
        self.body.setLinearVel(vel)

    def getVel(self):
        return self.body.getLinearVel()

    def setAngVel(self, angVel):
        self.body.setAngularVel(angVel)

    def getAngVel(self):
        return self.body.getAngularVel()
