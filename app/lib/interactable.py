from pandac.PandaModules import Point3, BitMask32, TransformState
from panda3d.bullet import BulletRigidBodyNode
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
 
        self.shapes = []

    def addShape(self, s, loc = Point3()):
        self.shapes += [s]
        self.node.addShape(s, TransformState.makePos(loc))
