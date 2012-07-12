from pandac.PandaModules import Point3
from ..lib.thing import Thing

class Key(Thing):
    def __init__(self, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        super(Key, self).__init__("key", loc)

        self.interval = self.model.hprInterval(5, Point3(0, 0, 360), startHpr = Point3(0,0,0))
        self.model.setScale(0.5)
        self.interval.loop()
