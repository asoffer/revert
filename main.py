from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, Vec3, WindowProperties, BitMask32, Fog, VBase4, DirectionalLight, TransformState
from direct.filter.CommonFilters import CommonFilters


from app.masters.cameraMaster import CameraMaster
from app.lib.levelBuilder import LevelBuilder
from app.lib.interactable import Interactable
from app.lib.pocketable import Pocketable
from app.lib.pocketer import Pocketer
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

        self.objs = []
        self.pockets = []

    def add(self, thing, loc = Point3()):
        if isinstance(thing, Interactable):
            thing.initialize(WORLD)
            self.objs += [thing]

            #FIXME maybe set Hpr as well for both of these?
        else:
            thing.model.reparentTo(render)

        if isinstance(thing, Pocketable):
           self.pockets += [thing]


    def initFilters(self):
        self.filters = CommonFilters(self.win, self.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.3, intensity=1.5, size="small")
        if (filterok == False):
            print "GPU not powerful enough to use bloom filter"
            return

    def initLightingAndGraphics(self):
        WORLD.fog.setColor(self.getBackgroundColor())
        WORLD.fog.setLinearOnsetPoint(0,0,0)
        WORLD.fog.setLinearOpaquePoint(0,Thing.REVERTS_VISIBLE * 3, 0)#THING_REVERT_DISTANCE)
        render.setFog(WORLD.fog)

        #initialize a hud
        self.hud = HUD()
        self.add(self.hud)

        self.lights = [DirectionalLight('l1'), DirectionalLight('l2')]
        for i in range(len(self.lights)):
            self.lights[i].setColor(VBase4(0.5, 0.5, 0.5, 1))
            n = render.attachNewNode(self.lights[i])
            n.setHpr(40 * i - 20, -40, 40) #FIXME tweak the lighting, maybe
            render.setLight(n)

 

    def initListeners(self):
        self.accept('s',lambda: messenger.send("save"))
        self.accept('r',lambda: messenger.send("revert"))
        self.accept('arrow_left', lambda: messenger.send("player_left_down"))
        self.accept('arrow_left-up', lambda: messenger.send("player_left_up"))
        self.accept('arrow_right', lambda: messenger.send("player_right_down"))
        self.accept('arrow_right-up', lambda: messenger.send("player_right_up"))
        self.accept('arrow_up', lambda: messenger.send("player_jump"))


    def update(self, task):
        WORLD.bw.doPhysics(self.dt, 5, 1.0/180.0)

        #constraints
        for thing in self.objs:
            thing.np.setY(0)
            thing.np.setH(0)
            thing.np.setP(0)

        self.player.np.setR(0)

        return task.cont

    def checkGhost(self, task):
        #FIXME only for player
        for x in self.pockets:
            if x.gNode.getNumOverlappingNodes() > 0:
                if self.player.node in x.gNode.getOverlappingNodes():
                    self.player.putInPocket(WORLD, x)
                    self.pockets.remove(x)

        return task.cont


GAME = Game("Revert")

#NOTE import must be done down here because World references the singleton 'render'
from app.world import *

LVLB = LevelBuilder(GAME)

LVLB.build("test")

GAME.player = Player(WORLD, loc = GAME.playerInitLoc)
GAME.add(GAME.player)

GAME.initLightingAndGraphics()
GAME.initFilters()


GAME.taskMgr.add(GAME.player.move, "movePlayer")
GAME.initListeners()


GAME.taskMgr.doMethodLater(1, GAME.update, "physics")

GAME.taskMgr.doMethodLater(1,GAME.checkGhost, "checkGhost")

GAME.run()
