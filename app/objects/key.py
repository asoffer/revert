from pandac.PandaModules import Point3
from ..lib.item import Item

class Key(Item):
    def __init__(self, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        super(Key, self).__init__("key", loc)

        self.model.setScale(0.5)