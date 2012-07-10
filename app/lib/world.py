from pandac.PandaModules import Fog, Point3, VBase4, AmbientLight
from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.core import Quat

from ..objects.player import Player
from ..objects.hud import HUD
from .thing import Thing
from .physical import Physical
from .touchable import Touchable

class World(object):
    def __init__(self, game):
        super(World, self).__init__()

        self.game = game


        self.things = []


        #initialize the rendering
        self.renderer = self.game.render
        self.initFog()

        #FIXME do better lighting
        alight = AmbientLight('alight')
        alight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        alnp = self.renderer.attachNewNode(alight)
        self.renderer.setLight(alnp)

        #initialize a hud
        self.hud = HUD()
        self.add(self.hud)

        #physics
        self.world = OdeWorld()
        self.world.setGravity(0,  -20, 0) #FIXME (0,-9.81) would be realistic physics

        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 0.6, 0.0, 9.1, 0.9, 0.00001, 1.0, 0.02) #FIXME I have no idea what this means

        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactGroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactGroup)

        self.timeAccumulator = 0
        self.dt = 1.0 / 60.0

        #give it a player
        self.player = Player(self, Point3(0,10,0))
        self.add(self.player)
        self.game.taskMgr.add(self.player.move, "movePlayer")

    def initFog(self):
        f = Fog("World Fog")
        f.setColor(0.5,0.5,0.5)
        f.setLinearOnsetPoint(0,0,0)
        f.setLinearOpaquePoint(0,0,-Thing.REVERTS_VISIBLE * 3)#THING_REVERT_DISTANCE)
        self.renderer.attachNewNode(f)
        self.renderer.setFog(f)

    def add(self, obj):
        obj.model.reparentTo(self.renderer)
        if isinstance(obj, Physical):
            self.things += [obj]

    def step(self, task):
        self.timeAccumulator += globalClock.getDt()
        while(self.timeAccumulator > self.dt):
            self.timeAccumulator -= self.dt

            self.space.autoCollide()
            self.world.quickStep(self.dt)
            self.contactGroup.empty()

        for x in self.things:
            x.constrainPosQuat()
            x.model.setPosQuat(self.renderer, x.body.getPosition(), Quat(x.body.getQuaternion()))

        return task.cont





