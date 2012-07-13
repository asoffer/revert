from .touchable import Touchable

class Pocketer(Touchable):
    """ 
    The Pocketer class is the base class for objects that can pick up Pocketable Items
    """

    def __init__(self):
        super(Pocketer, self).__init__()

        self.pocket = []

        self.geom.setCollideBits(BitMask32(0x00000011))

    def pocket(self, obj):
        self.pocket += [obj]

