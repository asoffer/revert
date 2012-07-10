from copy import deepcopy
from pandac.PandaModules import Point3, Vec3
from direct.showbase import DirectObject

THING_ID = 0
THING_REVERT_DISTANCE = 3

class Thing(object, DirectObject.DirectObject):
    """ 
    The Thing class is the base class for anything that is rendered on the screen.
    """

    REVERTS_VISIBLE = 8

    def __init__(self, model, loc = Point3()):
        super(Thing, self).__init__()
        DirectObject.DirectObject.__init__(self)

        global THING_ID
        THING_ID += 1

        #unique id and string id for message passing
        self.uid = THING_ID
        self.usid = "Thing" + str(self.uid)

        self.stack = []
        self.revertable = True

        #load the model
        self.modelPath = 'app/media/models/%s/%s.egg' % (model, model)
        self.model = base.loader.loadModel(self.modelPath)
        self.model.setPos(loc)

        #list of what to save and what to revert
        self.toRevert = {'model': self.setModel, 'location': self.setPos}
        self.toSave = {'model': self.getModel, 'location': self.getPos}

        #listen for saving and reverting
        self.accept("save", self.save)
        self.accept("revert", self.revert)

    def getModel(self):
        return self.model

    def setModel(self, m):
        self.model.detachNode()
        self.model = m
        self.model.reparentTo(base.render)

    def setPos(self, pos):
        self.model.setPos(pos)

    def getPos(self):
        return self.model.getPos()

    def setRevertable(self, b):
        """
        b is a boolean which determines whether or not an object reverts
        """

        self.revertable = b

    def save(self):
        """
        push state onto the stack
        """

        if not self.revertable:
            return

        state = {}
        for x in self.toSave:
            state[x] = deepcopy(self.toSave[x]())

        #made a new model, reparent it so it displays
        state["model"].reparentTo(base.render)

        #add it to the stack
        self.stack.append(state)

        for s in self.stack:
            s["model"].setPos(s["model"].getPos() + Vec3(0,0,-THING_REVERT_DISTANCE))

    def revert(self):
        """
        pop state from the stack
        """

        if len(self.stack) == 0 or not self.revertable:
            return

        for s in self.stack:
            s["model"].setPos(s["model"].getPos() + Vec3(0,0,THING_REVERT_DISTANCE))

        state = self.stack.pop()

        #not sure if this helps, but it can't hurt
        self.model.detachNode()

        for x in self.toRevert:
            self.toRevert[x](state[x])
