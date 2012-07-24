from pandac.PandaModules import Point3, Vec3, BitMask32, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode
from .thing import Thing

class Interactable(Thing):
    """ 
    The Interactable class is the base class for anything that needs to interact with the Player, or other things on screen. Basically, anything that isn't just a pretty image.
    """

    def __init__(self, model, loc = Point3(), revert = True, mass = 0.0):
        super(Interactable, self).__init__(model, loc = loc, revert = revert)
        self.node = BulletRigidBodyNode(self.usid)
        self.node.setMass(mass)

        self.initLoc = loc

        self.gNode = BulletGhostNode("Ghost" + self.usid)

        self.shapes = []
        self.ghostShapes = []

        self.np = None
        self.gnp = None

    def initialize(self, w):
        self.np = render.attachNewNode(self.node)
        w.bw.attachRigidBody(self.node)

        self.np.setPos(self.initLoc)
        self.model.reparentTo(self.np)
       
        self.gnp = self.np.attachNewNode(self.gNode)
        w.bw.attachGhost(self.gNode)

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
        self.node.addShape(shape, TransformState.makePosHpr(loc, Vec3(0, 0, rot)))

    def addGhostShape(self, shape, loc = Point3(), rot = 0):
        self.ghostShapes += [shape]
        self.gNode.addShape(shape, TransformState.makePosHpr(loc, Vec3(0,0, rot)))
