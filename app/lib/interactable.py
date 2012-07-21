from pandac.PandaModules import Point3, Vec3, BitMask32, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode
from .thing import Thing

class Interactable(Thing):
    """ 
    The Interactable class is the base class for anything that needs to interact with the Player, or other things on screen. Basically, anything that isn't just a pretty image.
    """

    def __init__(self, worldNP, model, loc = Point3(), revert = True, mass = 0.0):
        super(Interactable, self).__init__(model, loc = loc, revert = revert)
        self.np = worldNP[0].attachNewNode(BulletRigidBodyNode(self.usid))

        self.np.node().setMass(mass)
        self.np.setPos(loc)
        self.model.reparentTo(self.np)
        worldNP[1].attachRigidBody(self.np.node())

        self.gnp = worldNP[0].attachNewNode(BulletGhostNode("Ghost" + self.usid))
        worldNP[1].attachGhost(self.gnp.node())

        self.shapes = []
        self.ghostShapes = []

    def setPos(self, pos):
        self.np.setPos(pos)

    def getPos(self):
        return Point3(self.np.getPos())

    def setRot(self, rot):
        self.np.setHpr(rot)

    def getRot(self):
        return Vec3(self.np.getHpr())

    def addShape(self, shape, loc = Point3(), rot = 0):
        self.shapes += [shape]
        self.np.node().addShape(shape, TransformState.makePosHpr(loc, Vec3(0, 0, rot)))

    def addGhostShape(self, shape, loc = Point3(), rot = 0):
        self.ghostShapes += [shape]
        self.gnp.node().addShape(shape, TransformState.makePosHpr(loc + self.np.getPos(), Vec3(0,0, rot)))
