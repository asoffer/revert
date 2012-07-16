from pandac.PandaModules import Point3, BitMask32, Quat

from .interactable import Interactable

class Physical(Interactable):
    """ 
    The Physical class is the base class for anything that responds to physics
    """

    def __init__(self, model, loc = Point3(), revert = True, rot = True):
        super(Physical, self).__init__(model, loc = loc, revert = revert)

        if not rot:
            self.toRevert['rot'] = self.setRot
            self.toSave['rot'] = self.getRot
            self.toRevert['angVel'] = self.setAngVel
            self.toSave['angVel'] = self.getAngVel

        self.toRevert['vel'] = self.setVel
        self.toSave['vel'] = self.getVel

        self.node.setMass(1) #this default is lame and should be changed
        self.node.setActive(True)

        self.nodePath = base.render.attachNewNode(self.node)


    def getPos(self):
        return self.nodePath.getPos()

    def setPos(self, pos):
        return self.nodePath.setPos(pos)

    def setRot(self, rot):
        pass

    def getRot(self):
        pass

    def setVel(self, vel):
        pass

    def getVel(self):
        pass

    def setAngVel(self, angVel):
        pass

    def getAngVel(self):
        pass
