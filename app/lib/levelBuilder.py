from pandac.PandaModules import Point3, VBase3, Vec3, BitMask32

import xml.parsers.expat as expat
from ..objects.ball import  Ball
from ..objects.block import Block
from ..objects.platform import Platform
from ..objects.key import Key

from panda3d.bullet import BulletPlaneShape, BulletRigidBodyNode

class LevelBuilder(object):
    def __init__(self, game):

        self.game = game
        self.worldNP = [game.worldNP, game.world]

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
            thing = Ball(self.worldNP, loc = pointFromAttrs(attrs), revert = rev)
        elif name == "block":
            thing = Block(self.worldNP, loc = pointFromAttrs(attrs), revert = rev)
        elif name == "platform":
            thing = Platform(self.worldNP, float(attrs["width"]), float(attrs["rot"]), loc = pointFromAttrs(attrs))
        elif name == "wall":
            thing = Platform(self.worldNP, float(attrs["height"]), rot = 90, loc = pointFromAttrs(attrs))
        elif name == "key":
            thing = Key(self.worldNP, loc = pointFromAttrs(attrs), revert = rev)
        else:
            return

        self.game.add(thing, pointFromAttrs(attrs))

    def characterData(self, data):
        pass

    def endElement(self, name):
        pass


    def build(self, levelString):
        xmlFile = open("app/level/" + levelString + ".rvt", 'r')
        self.parser.ParseFile(xmlFile)
        xmlFile.close()


        
        
        plane = BulletPlaneShape(Vec3(0,0,1), 0)
        planeNP = self.game.worldNP.attachNewNode(BulletRigidBodyNode('Ground'))
        self.game.world.attachRigidBody(planeNP.node())
        planeNP.node().addShape(plane)
        print planeNP.getPos()
        planeNP.setCollideMask(BitMask32.allOn())

        
        self.game.setBackgroundColor(self.bg)

def pointFromAttrs(attrs):
    return Point3(float(attrs['x']), 0, float(attrs['y']))
