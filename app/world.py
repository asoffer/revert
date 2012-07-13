from pandac.PandaModules import Fog, Point3, VBase4, DirectionalLight, PointLight
from panda3d.ode import OdeWorld, OdeSimpleSpace, OdeJointGroup
from panda3d.core import Quat

from .objects.player import Player
from .objects.hud import HUD
from .lib.thing import Thing
from .lib.physical import Physical
from .lib.touchable import Touchable

import app.game

WORLD = None

class World(object):
    def __init__(self):
        super(World, self).__init__()

        self.things = []

        #initialize the rendering
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

    def setBackgroundColor(self, bg):
        app.game.GAME.setBackgroundColor(bg)

    def initWorldGraphics(self):
        self.fog.setColor(app.game.GAME.getBackgroundColor())
        self.fog.setLinearOnsetPoint(0,0,0)
        self.fog.setLinearOpaquePoint(0,0,-Thing.REVERTS_VISIBLE * 3)#THING_REVERT_DISTANCE)
        app.game.GAME.render.attachNewNode(self.fog)
        app.game.GAME.render.setFog(self.fog)

        #initialize a hud
        self.hud = HUD()
        self.add(self.hud)

        #initialize player
        self.player = Player(Point3(0,10,0))
        self.add(self.player)
        app.game.GAME.taskMgr.add(self.player.move, "movePlayer")



        self.lights = [DirectionalLight('l1'), DirectionalLight('l2')]
        for i in range(len(self.lights)):
            self.lights[i].setColor(VBase4(0.7, 0.7, 0.7, 1))
            n = app.game.GAME.render.attachNewNode(self.lights[i])
            n.setHpr(40 * i - 20, -120, 0)
            app.game.GAME.render.setLight(n)


    def add(self, obj):
        obj.model.reparentTo(app.game.GAME.render)
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
            x.model.setPosQuat(app.game.GAME.render, x.body.getPosition(), Quat(x.body.getQuaternion()))

        return task.cont

def initialize():
    global WORLD
    if WORLD == None:
        WORLD = World()

def initWorldGraphics():
    global WORLD
    if WORLD == None:
        raise WorldError("World has not been initialized yet!")

    WORLD.initWorldGraphics()

def add(obj):
    global WORLD
    if WORLD == None:
        raise WorldError("World has not been initialized yet!")

    WORLD.add(obj)

def step(task):
    global WORLD
    if WORLD == None:
        raise WorldError("World has not been initialized yet!")

    WORLD.step(task)

def setBackgroundColor(bg):
    global WORLD
    if WORLD == None:
        raise WorldError("World has not been initialized yet!")

    WORLD.setBackgroundColor(bg)

def getSpace():
    global WORLD
    if WORLD == None:
        raise WorldError("World has not been initialized yet!")

    return WORLD.space



class WorldError(Exception):
    def __init__(self, message):
        super(WorldError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message

