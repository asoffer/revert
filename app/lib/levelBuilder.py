from pandac.PandaModules import Point3

import xml.parsers.expat as expat
from ..objects.ball import Ball
from ..objects.block import Block
from ..objects.platform import Platform
from world import World

class LevelBuilder(object):
    def __init__(self, game):

        self.game = game
        self.world = None

        self.parser = expat.ParserCreate()
        self.parser.StartElementHandler = self.startElement
        self.parser.CharacterDataHandler = self.characterData
        self.parser.EndElementHandler = self.endElement

    def startElement(self, name, attrs):
        thing = None

        if name == "ball":
            thing = Ball(self.world, loc = pointFromAttrs(attrs))
        elif name == "block":
            thing = Block(self.world, loc = pointFromAttrs(attrs))
        elif name == "platform":
            thing = Platform(self.world, float(attrs["width"]), float(attrs["rot"]), loc = pointFromAttrs(attrs))
        else:
            return

        self.world.add(thing)

    def characterData(self, data):
        pass

    def endElement(self, name):
        pass


    def build(self, levelString):
        self.world = World(self.game)

        xmlFile = open("app/level/" + levelString + ".rvt", 'r')
        self.parser.ParseFile(xmlFile)
        xmlFile.close()

        self.game.cameraStalkee = self.world.player

        return self.world


def pointFromAttrs(attrs):
    return Point3(float(attrs['x']), float(attrs['y']), 0)
