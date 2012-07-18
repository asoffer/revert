from .interactable import Interactable
from .pocketable import Pocketable
from pandac.PandaModules import Point3, TransformState
from panda3d.bullet import BulletGhostNode

class Pocketer(Interactable):
    """ 
    The Pocketer class is the base class for objects that can pick up Pocketable Items
    """

    def __init__(self, model, loc = Point3(), revert = True):
        super(Pocketer, self).__init__(model, loc = loc, revert = revert)

        self.pocket = []

    def putInPocket(self, obj):
        if not isinstance(obj, Pocketable):
            return False

        self.pocket += [obj]
        obj.setOwner(self)

