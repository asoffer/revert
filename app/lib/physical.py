from pandac.PandaModules import Point3, Vec3

from .interactable import Interactable

class Physical(Interactable):
    """ 
    The Physical class is the base class for anything that responds to physics
    """

    def __init__(self, model, loc = Point3(), revert = True, rot = True):
        super(Physical, self).__init__(model, loc = loc, revert = revert)

        if rot:
            self.toRevert['angVel'] = self.setAngVel
            self.toSave['angVel'] = self.getAngVel

        self.toRevert['vel'] = self.setVel
        self.toSave['vel'] = self.getVel

        self.node.setMass(1) #this default is lame and should be changed
        self.node.setActive(True)

        self.nodePath = base.render.attachNewNode(self.node)
        self.nodePath.setPos(loc)

    def setVel(self, vel):
        self.node.setLinearVelocity(vel) #FIXME eh? almost working?

    def getVel(self):
        return Vec3(self.node.getLinearVelocity())

    def setAngVel(self, angVel):
        self.node.setAngularVelocity(angVel)

    def getAngVel(self):
        return Vec3(self.node.getAngularVelocity())
