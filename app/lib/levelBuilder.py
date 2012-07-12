from pandac.PandaModules import Point3, VBase3

import xml.parsers.expat as expat
from ..objects.ball import Ball
from ..objects.block import Block
from ..objects.platform import Platform
from ..objects.key import Key

from world import World

class LevelBuilder(object):
    def __init__(self, game):

        self.game = game
        self.world = None

        #default background color is the bland gray
        self.bg = VBase3(0.5,0.5,0.5)

        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.CharacterDataHandler = self.characterData
        self.parser.EndElementHandler = self.endElement

    def startElement(self, name, attrs):
        thing = None

        rev = not ("revert" in attrs and attrs["revert"] == "off")

        if name == "background":
            self.bg = VBase3(float(attrs['r']), float(attrs['g']), float(attrs['b']))
            return
        elif name == "ball":
            thing = Ball(self.game, loc = pointFromAttrs(attrs), revert = rev)
        elif name == "block":
            thing = Block(self.game, loc = pointFromAttrs(attrs), revert = rev)
        elif name == "platform":
            thing = Platform(self.game, float(attrs["width"]), float(attrs["rot"]), loc = pointFromAttrs(attrs))
        elif name == "key":
            thing = Key(self.game, loc = pointFromAttrs(attrs), revert = rev)
        else:
            return

        self.world.add(thing)

    def characterData(self, data):
        pass

    def endElement(self, name):
        pass


    def build(self, levelString):
        self.world = World(self.game)
        self.game.world = self.world

        xmlFile = open("app/level/" + levelString + ".rvt", 'r')
        self.parser.ParseFile(xmlFile)
        xmlFile.close()

        self.world.initPlayer()

        self.game.cameraStalkee = self.world.player
        self.world.setBackgroundColor(self.bg)

        return self.world


def pointFromAttrs(attrs):
    return Point3(float(attrs['x']), float(attrs['y']), 0)
