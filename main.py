from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, WindowProperties

from app.lib.world import World 
from app.lib.levelBuilder import LevelBuilder
from app.masters.cameraMaster import CameraMaster

class Game(ShowBase, CameraMaster):
    def __init__(self):
        ShowBase.__init__(self)
        CameraMaster.__init__(self)

        self.setWindowName("Revert")
        self.setBackgroundColor(0.5,0.5,0.5)

        self.levelBuilder = LevelBuilder(self)

        #key listening
        self.accept('s',lambda: messenger.send("save"))
        self.accept('r',lambda: messenger.send("revert"))
        self.accept('arrow_left', lambda: messenger.send("player_left_down"))
        self.accept('arrow_left-up', lambda: messenger.send("player_left_up"))
        self.accept('arrow_right', lambda: messenger.send("player_right_down"))
        self.accept('arrow_right-up', lambda: messenger.send("player_right_up"))
        self.accept('arrow_up', lambda: messenger.send("player_jump"))


    def setWindowName(self, name):
        props = WindowProperties()
        props.setTitle(name)
        base.win.requestProperties(props)

    def build(self, lvlString):
        self.world = self.levelBuilder.build(lvlString)

APP = Game()

APP.build("test")

APP.taskMgr.doMethodLater(0.1, APP.world.step, "physics")

APP.run()

