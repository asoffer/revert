from pandac.PandaModules import Point3, Vec3

from ..lib.pocketer import Pocketer
from ..lib.physical import Physical
from panda3d.bullet import BulletCapsuleShape, ZUp

class Player(Physical, Pocketer):
    def __init__(self, w, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """
        super(Player, self).__init__("player", loc = loc, revert = False)

        self.addShape(BulletCapsuleShape(1, 3, ZUp))

        #self.addGhostShape(BulletCapsuleShape(0.6, 3, ZUp), loc = Point3(0, 0, -1.3))

        self.key = {"left": False, "right": False}
        self.vel = Vec3(7, 0, 0)

        self.accept("player_left_down", self.setKey, ["left", True])
        self.accept("player_left_up", self.setKey, ["left", False])
        self.accept("player_right_down", self.setKey, ["right", True])
        self.accept("player_right_up", self.setKey, ["right", False])
        self.accept("player_jump", self.jump)

    def initialize(self, w):
        super(Player, self).initialize(w)

        self.world = w.bw

    def setKey(self, k, v):
        self.key[k] = v

    def move(self, task):
        if self.key["left"] and not self.key["right"]:
            self.vel.setX(-7)
        elif self.key["right"] and not self.key["left"]:
            self.vel.setX(7)
        else:
            self.vel.setX(0)

        v = Vec3(self.node.getLinearVelocity())
        v.setX(self.vel.getX())
        self.node.setLinearVelocity(v)

        return task.cont

    def jump(self):
        result = self.world.rayTestClosest(self.np.getPos() - Vec3(0,0, 2) , self.np.getPos() - Vec3(0, 0, 2.5))
        if result.hasHit():
            self.node.setLinearVelocity(Vec3(0, 0, 10))
