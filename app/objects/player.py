from pandac.PandaModules import Point3, Vec3
from panda3d.bullet import BulletCharacterControllerNode, BulletCapsuleShape, ZUp

from ..lib.pocketer import Pocketer

class Player(Pocketer):
    def __init__(self, worldNP, world, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """
        super(Player, self).__init__("player", loc = loc, revert = False)
        
        self.node = BulletCharacterControllerNode(BulletCapsuleShape(1, 3, ZUp), 0.4, 'player')

        self.nodePath = worldNP.attachNewNode(self.node)

        self.model.reparentTo(self.nodePath)

        self.key = {"left": False, "right": False}

        self.direction = 0
        self.speed = 7
        self.accept("player_left_down", self.setKey, ["left", True])
        self.accept("player_left_up", self.setKey, ["left", False])
        self.accept("player_right_down", self.setKey, ["right", True])
        self.accept("player_right_up", self.setKey, ["right", False])
        self.accept("player_jump", self.jump)

        world.attachCharacter(self.node)

        self.nodePath.setPos(loc)

    def setKey(self, k, v):
        self.key[k] = v

    def move(self, task):
        if self.key["left"] and not self.key["right"]:
            self.direction = -1
        elif self.key["right"] and not self.key["left"]:
            self.direction = 1
        else:
            self.direction = 0

        self.node.setLinearMovement(Vec3(self.speed * self.direction, 0, 0), True)

        return task.cont

    def jump(self):
        if self.node.isOnGround():
            self.node.setMaxJumpHeight(5.0)
            self.node.setJumpSpeed(8.0)
            self.node.doJump()
