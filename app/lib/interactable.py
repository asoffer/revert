from pandac.PandaModules import Point3, BitMask32
from .thing import Thing


class Interactable(Thing):
    """ 
    The Interactable class is the base class for anything that needs to interact with the Player, or other things on screen. Basically, anything that isn't just a pretty image.
    """

    def __init__(self, model, loc = Point3(), revert = True):
        super(Interactable, self).__init__(model, loc = loc, revert = revert)

        self.geoms = []

    def addGeom(self, geom, loc, bitMask):
        geom.setPosition(loc)
        geom.setCollideBits(BitMask32(bitMask))
        self.geoms += [geom]


