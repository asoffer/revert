from pandac.PandaModules import Vec3, Fog
from panda3d.bullet import BulletWorld, BulletDebugNode


class WORLD(object):
    def __call__(self):
        return self

    def __init__(self):
        super(WORLD, self).__init__()

        #Fog for the world
        self.fog = Fog("world fog")
        self.fogNP = render.attachNewNode(self.fog)

        self.np = self.fogNP.attachNewNode('World')
        self.dnp = self.np.attachNewNode(BulletDebugNode('Debug'))
        self.dnp.show()

        self.bw = BulletWorld()
        self.bw.setGravity(Vec3(0, 0, -9.81))
        self.bw.setDebugNode(self.dnp.node())

        self.dnp.node().showWireframe(True)
        self.dnp.node().showConstraints(True)
        self.dnp.node().showBoundingBoxes(False)
        self.dnp.node().showNormals(False)

WORLD = WORLD()
