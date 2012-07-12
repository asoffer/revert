from pandac.PandaModules import Fog, Point3, VBase4, DirectionalLight, PointLight
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
        self.fog = Fog("world fog")
        
        #physics
        self.world = OdeWorld()
        self.world.setGravity(0,  -20, 0) #FIXME (0,-9.81) would be realistic physics

        self.world.initSurfaceTable(1)
        self.world.setSurfaceEntry(0, 0, 0.8, 0.0, 9.1, 0.9, 0.00001, 1.0, 0.02) #FIXME I have no idea what this means

        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactGroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactGroup)

        self.timeAccumulator = 0
        self.dt = 1.0 / 60.0

    def initPlayer(self):
        #give it a player
        self.player = Player(self.game, Point3(0,10,0))
        self.add(self.player)
        self.game.taskMgr.add(self.player.move, "movePlayer")

    def setBackgroundColor(self, bg):
        self.game.setBackgroundColor(bg)

    def init(self):
        self.fog.setColor(self.game.getBackgroundColor())
        self.fog.setLinearOnsetPoint(0,0,0)
        self.fog.setLinearOpaquePoint(0,0,-Thing.REVERTS_VISIBLE * 3)#THING_REVERT_DISTANCE)
        self.renderer.attachNewNode(self.fog)
        self.renderer.setFog(self.fog)

        #initialize a hud
        self.hud = HUD(self.game)
        self.add(self.hud)

        self.lights = [DirectionalLight('l1'), DirectionalLight('l2')]
        for i in range(len(self.lights)):
            self.lights[i].setColor(VBase4(0.7, 0.7, 0.7, 1))
            n = self.renderer.attachNewNode(self.lights[i])
            n.setHpr(40 * i - 20, -120, 0)
            self.renderer.setLight(n)


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





