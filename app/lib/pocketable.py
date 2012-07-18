from pandac.PandaModules import Point3, TransformState

from .interactable import Interactable

class Pocketable(Interactable):
    """ 
    The Pocketable class is the base class for objects that can be picked up Pocketers
    """

    def __init__(self, model, loc, revert):
        super(Pocketable, self).__init__(model, loc = loc, revert = revert)

        self.owner = None

        self.toSave["owner"] = self.getOwner
        self.toRevert["owner"] = self.setOwner

    def getOwner(self):
        return self.owner

    def setOwner(self, p):
        if self.owner == None and p != None:
            self.model.hide()
            #FIXME and remove ghost nodes
        elif self.owner != None and p == None:
            self.model.show()
            #FIXME and put ghost nodes back
        self.owner = p
