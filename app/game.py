from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, WindowProperties, TextureStage

from direct.filter.CommonFilters import CommonFilters

from lib.levelBuilder import LevelBuilder
from masters.cameraMaster import CameraMaster

GAME = None

class Game(ShowBase, CameraMaster):
    def __init__(self):
        ShowBase.__init__(self)
        CameraMaster.__init__(self)

        self.setWindowName("Revert")

        self.levelBuilder = LevelBuilder()

        #key listening
        self.accept('s',lambda: messenger.send("save"))
        self.accept('r',lambda: messenger.send("revert"))
        self.accept('arrow_left', lambda: messenger.send("player_left_down"))
        self.accept('arrow_left-up', lambda: messenger.send("player_left_up"))
        self.accept('arrow_right', lambda: messenger.send("player_right_down"))
        self.accept('arrow_right-up', lambda: messenger.send("player_right_up"))
        self.accept('arrow_up', lambda: messenger.send("player_jump"))

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
        self.levelBuilder.build(lvlString)

def initialize():
    global GAME, loader, noGlow, noGlowTextureStage, glow, glowTextureStage
    if GAME == None:
        GAME = Game()

    loader = GAME.loader

    noGlow = loader.loadTexture("app/media/effects/empty.png")
    noGlowTextureStage = TextureStage('noGlow')
    noGlowTextureStage.setMode(TextureStage.MModulateGlow)

    glow = loader.loadTexture("app/media/effects/red.png")
    glowTextureStage = TextureStage('glow')
    glowTextureStage.setMode(TextureStage.MModulateGlow)

def initFilters():
    global GAME
    if GAME == None:
        raise WorldError("Game has not been initialized yet!")

    GAME.initFilters()

def setWindowName(name):
    global GAME
    if GAME == None:
        raise WorldError("Game has not been initialized yet!")

    GAME.setWindowName(name)

def build(lvlString):
    global GAME
    if GAME == None:
        raise WorldError("Game has not been initialized yet!")

    GAME.build(lvlString)

class GameError(Exception):
    def __init__(self, message):
        super(GameError, self).__init__()
        self.message = message

    def __str__(self):
        return self.message

