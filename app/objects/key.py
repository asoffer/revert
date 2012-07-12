from pandac.PandaModules import Point3
from ..lib.item import Item

class Key(Item):
    def __init__(self, game, loc = Point3(), revert = True):
        """
        the location is the bottom-left corner of the platform
        """

        super(Key, self).__init__(game, "key", loc, revert)
       
