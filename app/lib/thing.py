from copy import deepcopy
from pandac.PandaModules import Point3, Vec3, TextureStage, NodePath
from direct.showbase import DirectObject

THING_ID = 0
THING_REVERT_DISTANCE = 3

class Thing(object, DirectObject.DirectObject):
    """ 
    The Thing class is the base class for anything that is rendered on the screen.
    """

    REVERTS_VISIBLE = 8

    def __init__(self, model, loc = Point3(), revert = True):
        super(Thing, self).__init__()
        DirectObject.DirectObject.__init__(self)

        global THING_ID
        THING_ID += 1

        #unique id and string id for message passing
        self.uid = THING_ID
        self.usid = "Thing" + str(self.uid)

        self.stack = []
        self.revertable = revert

        #load the model
        self.modelPath = 'app/media/models/%s/%s.egg' % (model, model)
        self.model = loader.loadModel(self.modelPath)
        self.nodePath = self.model
        self.node = self.nodePath.node()

        ##################### FIXME this should be global.
        noGlow = loader.loadTexture("app/media/effects/empty.png")
        noGlowTextureStage = TextureStage('noGlow')
        noGlowTextureStage.setMode(TextureStage.MModulateGlow)

        glow = loader.loadTexture("app/media/effects/red.png")
        glowTextureStage = TextureStage('glow')
        glowTextureStage.setMode(TextureStage.MModulateGlow)
        ##################### END FIXME

        if self.revertable:
            self.model.setTexture(noGlowTextureStage, noGlow)
        else:
            self.model.setTexture(glowTextureStage, glow)

        #list of what to save and what to revert
        self.toRevert = {'pos': self.setPos, 'rot': self.setRot}
        self.toSave = {'pos': self.getPos, 'rot': self.getRot}

        #listen for saving and reverting
        self.accept("save", self.save)
        self.accept("revert", self.revert)

    def setPos(self, pos):
        self.nodePath.setPos(pos)

    def getPos(self):
        return Point3(self.nodePath.getPos())

    def setRot(self, rot):
        self.nodePath.setHpr(rot)

    def getRot(self):
        return Vec3(self.nodePath.getHpr())

    def save(self):
        """
        push state onto the stack
        """

        if not self.revertable:
            return


        state = {}
        for x in self.toSave:
            state[x] = self.toSave[x]()

        state["model"] = deepcopy(self.model)
        state["model"].reparentTo(base.render)
        state["model"].setPos(self.nodePath.getPos())
        state["model"].setHpr(self.nodePath.getHpr())
 
        #add it to the stack
        self.stack.append(state)

        for s in self.stack:
            s["model"].setY(s["model"].getY() + THING_REVERT_DISTANCE)

    def revert(self):
        """
        pop state from the stack
        """

        if len(self.stack) == 0 or not self.revertable:
            return

        for s in self.stack:
            s["model"].setY(s["model"].getY() - THING_REVERT_DISTANCE)

        state = self.stack.pop()

        state["model"].removeNode()

        for x in self.toRevert:
            self.toRevert[x](state[x])
