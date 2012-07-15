from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, Vec3, WindowProperties, BitMask32, Fog, VBase4, DirectionalLight
from direct.filter.CommonFilters import CommonFilters

from panda3d.bullet import BulletWorld, BulletDebugNode


from app.masters.cameraMaster import CameraMaster
from app.lib.levelBuilder import LevelBuilder
from app.lib.interactable import Interactable
from app.lib.thing import Thing
from app.objects.hud import HUD



class Game(ShowBase, CameraMaster):
    def __init__(self, title):
        ShowBase.__init__(self)
        CameraMaster.__init__(self)

        self.dt = 1.0 / 60.0

        props = WindowProperties()
        props.setTitle(title)
        self.win.requestProperties(props)

        self.setFrameRateMeter(True)

        self.worldNP = render.attachNewNode('World')
        self.debugNP = self.worldNP.attachNewNode(BulletDebugNode('Debug'))
 
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, -9.81, 0))
        self.world.setDebugNode(self.debugNP.node())

    def build(self, lvlString):
        LevelBuilder(self).build(lvlString)

    def add(self, thing, loc):
        if isinstance(thing, Interactable):
            thing.nodePath = self.worldNP.attachNewNode(thing.node)
            thing.nodePath.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(thing.nodePath.node())
        if isinstance(thing, Thing):
            thing.model.reparentTo(thing.nodePath)
            thing.nodePath.setPos(loc)

    def initFilters(self):
        self.filters = CommonFilters(self.win, self.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.3, intensity=1.5, size="small")
        if (filterok == False):
            print "GPU not powerful enough to use bloom filter"
            return

    def initLightingAndGraphics(self):
        self.fog = Fog("world fog")
        self.fog.setColor(self.getBackgroundColor())
        self.fog.setLinearOnsetPoint(0,0,0)
        self.fog.setLinearOpaquePoint(0,0,-Thing.REVERTS_VISIBLE * 3)#THING_REVERT_DISTANCE)
        render.attachNewNode(self.fog)
        render.setFog(self.fog)

        #initialize a hud
        self.hud = HUD()
        #self.add(self.hud)

        #initialize player
        #self.player = Player(Point3(0,10,0))
        #self.add(self.player)
        #self.taskMgr.add(self.player.move, "movePlayer")

        self.lights = [DirectionalLight('l1'), DirectionalLight('l2')]
        for i in range(len(self.lights)):
            self.lights[i].setColor(VBase4(0.7, 0.7, 0.7, 1))
            n = render.attachNewNode(self.lights[i])
            n.setHpr(40 * i - 20, -120, 0)
            render.setLight(n)

    def update(self, task):
        self.world.doPhysics(self.dt, 5, 1.0/180.0)
        return task.cont



GAME = Game("Revert")
GAME.build("test")

GAME.initLightingAndGraphics()
GAME.initFilters()

GAME.taskMgr.doMethodLater(0.1, GAME.update, "physics")

GAME.run()



"""
World.initWorldGraphics()



Game.GAME.taskMgr.doMethodLater(0.1, World.WORLD.step, "physics")


Game.GAME.cameraStalkee = World.WORLD.player
Game.GAME.run()
"""
