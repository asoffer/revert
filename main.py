import app.game as Game
import app.world as World

Game.initialize()
World.initialize()

Game.build("test")

World.initWorldGraphics()

Game.initFilters()

Game.GAME.taskMgr.doMethodLater(0.1, World.WORLD.step, "physics")

Game.GAME.cameraStalkee = World.WORLD.player
Game.GAME.run()
