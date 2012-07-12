from pandac.PandaModules import Point3, Vec3, VBase3
from panda3d.ode import OdeBoxGeom, OdeMass

from ..lib.physical import Physical

class Player(Physical):
    def __init__(self, world, loc = Point3()):
        """
        the location is the bottom-left corner of the platform
        """

        geom = OdeBoxGeom(world.space, 2,5,2)
        mass = OdeMass()
        mass.setBox(1000, 2, 5, 2)

        super(Player, self).__init__(world, mass, geom, "player", loc, False)

        self.setRevertable(False)

        self.key = {"left": False, "right": False}

        self.direction = 0
        self.speed = 10

        self.accept("player_left_down", self.setKey, ["left", True])
        self.accept("player_left_up", self.setKey, ["left", False])
        self.accept("player_right_down", self.setKey, ["right", True])
        self.accept("player_right_up", self.setKey, ["right", False])
        self.accept("player_jump", self.jump)


    def setKey(self, k, v):
        self.key[k] = v

    def move(self, task):
        if self.key["left"] and not self.key["right"]:
            self.direction = -1
        elif self.key["right"] and not self.key["left"]:
            self.direction = 1
        else:
            self.direction = 0

        if self.body.getLinearVel()[0] * self.direction < 20:
            self.body.addRelForce(VBase3(10000000*self.direction, 0,0))#setLinearVel(self.direction * self.speed, self.body.getLinearVel().getY(), 0)

        return task.cont

    def jump(self):
        self.body.setLinearVel(self.body.getLinearVel() + VBase3(0,10,0))
