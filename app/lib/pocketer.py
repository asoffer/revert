from .pocketable import Pocketable

class Pocketer(object):
    """ 
    The Pocketer class is the base class for objects that can pick up Pocketable Items
    """

    def __init__(self):
        super(Pocketer, self).__init__()

        self.pocket = []

    def putInPocket(self, world, obj):
        if not isinstance(obj, Pocketable):
            return False

        self.pocket += [obj]
        obj.setOwner(world, self)

