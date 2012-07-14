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

    def addGeom(self, geom, loc):
        super(Pocketable, self).addGeom(geom, loc, 2)

    def getOwner(self):
        return self.owner

    def setOwner(self, p):
        if self.owner == None and p != None:
            self.model.show()
        elif self.owner != None and p == None:
            self.model.hide()
        self.owner = p
