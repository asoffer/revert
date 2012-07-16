from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, Vec3, WindowProperties, BitMask32, Fog, VBase4, DirectionalLight
from direct.filter.CommonFilters import CommonFilters

from panda3d.bullet import BulletWorld, BulletDebugNode


from app.masters.cameraMaster import CameraMaster
from app.lib.levelBuilder import LevelBuilder
from app.lib.interactable import Interactable
from app.lib.thing import Thing
from app.objects.hud import HUD
from app.objects.player import Player


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
        self.debugNP.node().showWireframe(True)
        self.debugNP.node().showConstraints(True)
        self.debugNP.node().showBoundingBoxes(False)
        self.debugNP.node().showNormals(False)
        self.debugNP.show()

    def build(self, lvlString):
        LevelBuilder(self).build(lvlString)

    def add(self, thing, loc = Point3()):
        if isinstance(thing, Interactable):
            thing.nodePath = self.worldNP.attachNewNode(thing.node)
            thing.nodePath.setCollideMask(BitMask32.allOn())
            self.world.attachRigidBody(thing.nodePath.node())
            thing.model.reparentTo(thing.nodePath)
            thing.nodePath.setPos(loc)
        else:
            thing.model.reparentTo(render)
 


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
        self.add(self.hud)

        self.lights = [DirectionalLight('l1'), DirectionalLight('l2')]
        for i in range(len(self.lights)):
            self.lights[i].setColor(VBase4(0.7, 0.7, 0.7, 1))
            n = render.attachNewNode(self.lights[i])
            n.setHpr(40 * i - 20, -120, 0)
            render.setLight(n)

    def initPlayer(self, loc):
        self.player = Player(loc)
        self.add(self.player, loc)
        self.taskMgr.add(self.player.move, "movePlayer")

    def initListeners(self):
        self.accept('s',lambda: messenger.send("save"))
        self.accept('r',lambda: messenger.send("revert"))
        self.accept('arrow_left', lambda: messenger.send("player_left_down"))
        self.accept('arrow_left-up', lambda: messenger.send("player_left_up"))
        self.accept('arrow_right', lambda: messenger.send("player_right_down"))
        self.accept('arrow_right-up', lambda: messenger.send("player_right_up"))
        self.accept('arrow_up', lambda: messenger.send("player_jump"))


    def update(self, task):
        self.world.doPhysics(self.dt, 5, 1.0/180.0)
        return task.cont



GAME = Game("Revert")
GAME.build("test")

GAME.initLightingAndGraphics()
GAME.initFilters()

GAME.initPlayer(Point3(0, 10, 0))
GAME.initListeners()


GAME.taskMgr.doMethodLater(0.1, GAME.update, "physics")

GAME.run()



"""
World.initWorldGraphics()



Game.GAME.taskMgr.doMethodLater(0.1, World.WORLD.step, "physics")


Game.GAME.cameraStalkee = World.WORLD.player
Game.GAME.run()
"""
