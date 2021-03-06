from pandac.PandaModules import Point3, BitMask32
from .thing import Thing

class Touchable(Thing):
    """ 
    The Touchable class is the base class for anything that can be touched/physically interacts with something else presence
    """

    def __init__(self, world, geom, model, loc = Point3()):
        super(Touchable, self).__init__(model, loc)

        #if it's also physical, this will not be the last call, based on the order of things
        self.setRevertable(False)

        self.geom = geom
        self.geom.setCollideBits(BitMask32(0x00000001))
