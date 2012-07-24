from pandac.PandaModules import Point3, TransformState

from .interactable import Interactable


class Pocketable(Interactable):
    """ 
    The Pocketable class is the base class for objects that can be picked up Pocketers
    """

    def __init__(self, model, loc = Point3(), revert = True):
        super(Pocketable, self).__init__(model, loc = loc, revert = revert)

        self.owner = None

        self.toSave["owner"] = self.getOwner
        self.toRevert["owner"] = self.setOwner

    def getOwner(self):
        return self.owner

    def setOwner(self, w, p):
        if self.owner == None and p != None:
            self.model.hide()
            w.bw.removeGhost(self.gNode)
            w.bw.removeRigidBody(self.node)

        #FIXME what else can happen
