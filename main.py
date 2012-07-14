import app.game as Game
import app.world as World

def onCollision(entry):
    geom1 = entry.getGeom1()
    geom2 = entry.getGeom2()
    body1 = entry.getBody1()
    body2 = entry.getBody2()
    print "?? collision with " + str(geom1) + " and " + str(geom2)


Game.initialize()
World.initialize()

Game.build("test")

World.initWorldGraphics()

Game.initFilters()

Game.GAME.taskMgr.doMethodLater(0.1, World.WORLD.step, "physics")

World.WORLD.space.setCollisionEvent("ode-collision")
Game.GAME.accept("ode-collision", onCollision)



Game.GAME.cameraStalkee = World.WORLD.player
Game.GAME.run()


