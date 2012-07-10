from direct.showbase.ShowBase import ShowBase
from pandac.PandaModules import Point3, WindowProperties

from app.lib.world import World 
from app.objects.ball import Ball
from app.objects.block import Block
from app.objects.platform import Platform
from app.objects.player import Player
from app.masters.cameraMaster import CameraMaster

class Game(ShowBase, CameraMaster):
    def __init__(self):
        ShowBase.__init__(self)
        CameraMaster.__init__(self)

        self.setWindowName("Revert")
        self.setBackgroundColor(0.5,0.5,0.5)


        #key listening
        self.accept('s',lambda: messenger.send("save"))
        self.accept('r',lambda: messenger.send("revert"))
        self.accept('arrow_left', lambda: messenger.send("player_left_down"))
        self.accept('arrow_left-up', lambda: messenger.send("player_left_up"))
        self.accept('arrow_right', lambda: messenger.send("player_right_down"))
        self.accept('arrow_right-up', lambda: messenger.send("player_right_up"))
        self.accept('arrow_up', lambda: messenger.send("player_jump"))


        #make a world
        self.world = World(self)

        self.cameraStalkee = self.world.player

    def setWindowName(self, name):
        props = WindowProperties()
        props.setTitle(name)
        base.win.requestProperties(props)

APP = Game()
p = Platform(APP.world, Point3(0,0,0))
APP.world.add(p)

APP.taskMgr.add(APP.world.step, "physics")
#b = Block(APP.world, Point3(-5,30,0))
#APP.world.add(b)

b2 = Ball(APP.world, Point3(-5,20,0))
APP.world.add(b2)

APP.run()
