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

        self.setBackgroundColor(Point3(0.7,0.8,0.9))



        self.noGlow = self.loader.loadTexture("app/media/effects/empty.png")
        self.noGlowTextureStage = TextureStage('noGlow')
        self.noGlowTextureStage.setMode(TextureStage.MModulateGlow)

        self.glow = self.loader.loadTexture("app/media/effects/red.png")
        self.glowTextureStage = TextureStage('glow')
        self.glowTextureStage.setMode(TextureStage.MModulateGlow)



        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setBloom(blend=(0,0,0,1), desat=-0.5, intensity=3.0, size="small")
        if (filterok == False):
            addTitle("Toon Shader: Video card not powerful enough to do image postprocessing")
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

APP.taskMgr.doMethodLater(0.1, APP.world.step, "physics")

APP.run()

