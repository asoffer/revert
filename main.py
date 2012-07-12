from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, WindowProperties, TextureStage

from app.lib.world import World 
from app.lib.levelBuilder import LevelBuilder
from app.masters.cameraMaster import CameraMaster

from direct.filter.CommonFilters import CommonFilters

class Game(ShowBase, CameraMaster):
    def __init__(self):
        ShowBase.__init__(self)
        CameraMaster.__init__(self)

        self.setWindowName("Revert")

        self.levelBuilder = LevelBuilder(self)

        #key listening
        self.accept('s',lambda: messenger.send("save"))
        self.accept('r',lambda: messenger.send("revert"))
        self.accept('arrow_left', lambda: messenger.send("player_left_down"))
        self.accept('arrow_left-up', lambda: messenger.send("player_left_up"))
        self.accept('arrow_right', lambda: messenger.send("player_right_down"))
        self.accept('arrow_right-up', lambda: messenger.send("player_right_up"))
        self.accept('arrow_up', lambda: messenger.send("player_jump"))

        self.noGlow = self.loader.loadTexture("app/media/effects/empty.png")
        self.noGlowTextureStage = TextureStage('noGlow')
        self.noGlowTextureStage.setMode(TextureStage.MModulateGlow)

        self.glow = self.loader.loadTexture("app/media/effects/red.png")
        self.glowTextureStage = TextureStage('glow')
        self.glowTextureStage.setMode(TextureStage.MModulateGlow)

    def initFilters(self):
        self.filters = CommonFilters(self.win, self.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.3, intensity=1.5, size="small")
        if (filterok == False):
            print "GPU not powerful enough to use bloom filter"
            return
 

    def setWindowName(self, name):
        props = WindowProperties()
        props.setTitle(name)
        base.win.requestProperties(props)

    def build(self, lvlString):
        self.world = self.levelBuilder.build(lvlString)

APP = Game()

APP.build("test")
APP.world.init()
APP.initFilters()

APP.taskMgr.doMethodLater(0.1, APP.world.step, "physics")

APP.run()

