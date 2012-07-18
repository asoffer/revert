from pandac.PandaModules import Point3, Vec3, BitMask32, TransformState
from panda3d.bullet import BulletRigidBodyNode, BulletGhostNode
from .thing import Thing

class Interactable(Thing):
    """ 
    The Interactable class is the base class for anything that needs to interact with the Player, or other things on screen. Basically, anything that isn't just a pretty image.
    """

    def __init__(self, model, loc = Point3(), revert = True):
        super(Interactable, self).__init__(model, loc = loc, revert = revert)

        #usid already defined because super is already called (all the way up to Thing)
        self.node = BulletRigidBodyNode(self.usid)
        self.node.setMass(0) #this default should be changed every time if you want it to have finite mass

        self.ghostNode = BulletGhostNode("Ghost" + self.usid)
 
        self.shapes = []
        self.ghostShapes = []

    def addShape(self, shape, loc = Point3(), rot = 0):
        self.shapes += [shape]
        self.node.addShape(shape, TransformState.makePosHpr(loc, Vec3(0, 0, rot)))

    def addGhostShape(self, shape, loc = Point3(), rot = 0):
        self.ghostShapes += [shape]
        self.ghostNode.addShape(shape, TransformState.makePosHpr(loc, Vec3(0,0, rot)))


