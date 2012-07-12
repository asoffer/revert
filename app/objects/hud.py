from direct.gui.OnscreenText import OnscreenText
from ..lib.thing import Thing

class HUD(Thing):
    def __init__(self, game):
        super(HUD, self).__init__(game, "empty")

        #initialize hud
        self.textStackSize = OnscreenText(text = u"0/\u221e", pos = (-1.2, 0.9), scale = 0.07)
        self.stackDepth = 0

    def save(self):
        self.textStackSize.destroy()
        self.stackDepth += 1
        self.textStackSize = OnscreenText(text = str(self.stackDepth) + u"/\u221e", pos = (-1.2, 0.9), scale = 0.07)

    def revert(self):
        if self.stackDepth == 0:
            return

        self.textStackSize.destroy()
        self.stackDepth += -1
        self.textStackSize = OnscreenText(text = str(self.stackDepth) + u"/\u221e", pos = (-1.2, 0.9), scale = 0.07)
