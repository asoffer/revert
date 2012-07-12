from .thing import Thing

from pandac.PandaModules import Point3, Vec3

class Item(Thing):
    """ 
    The Item class is the base class for objects like keys, scrolls, etc... 
    """


    def __init__(self, game, model, loc = Point3(), revert = True):
        super(Item, self).__init__(game, model, loc, revert)

        self.interval = None

        self.setInterval(Point3())

    def setModel(self, m):
        #this is a faster way to keep track of the rotation... don't save and revert the intervals. just make a new one starting at the same rotation
        self.interval.finish()

        self.model.detachNode()
        self.model = m
        self.model.reparentTo(base.render)

        #model properties are preserved, because we just keep the model. it's okay to do this, because this item won't have any body attached to it
        self.setInterval(self.model.getHpr())

    def setRot(self, rot):
        self.model.setHpr(rot)

    def getRot(self):
        return self.model.getHpr()

    def setInterval(self, startRot):
        self.interval = self.model.hprInterval(6, startRot + Vec3(0, 0, 360), startHpr = startRot)
        self.interval.loop()



