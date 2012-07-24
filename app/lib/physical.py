from pandac.PandaModules import Point3, Vec3

from .interactable import Interactable

class Physical(Interactable):
    """ 
    The Physical class is the base class for anything that responds to physics
    """

    def __init__(self, model, loc = Point3(), revert = True, rot = True):
        super(Physical, self).__init__(model, mass = 1.0, loc = loc, revert = revert)

        if rot:
            self.toRevert['angVel'] = self.setAngVel
            self.toSave['angVel'] = self.getAngVel

        self.toRevert['vel'] = self.setVel
        self.toSave['vel'] = self.getVel

        self.node.setMass(1) #FIXME lame default mass

    def setVel(self, vel):
        self.np.node().setLinearVelocity(vel)

    def getVel(self):
        return Vec3(self.np.node().getLinearVelocity())

    def setAngVel(self, angVel):
        self.np.node().setAngularVelocity(angVel)

    def getAngVel(self):
        return Vec3(self.np.node().getAngularVelocity())
