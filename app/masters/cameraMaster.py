from direct.task import Task

class CameraMaster(object):
    def __init__(self):
        self.cameraZoom = -78

        # Disable the camera trackball controls.
        self.disableMouse()

        self.initCamera()

        self.cameraStalkee = None
        self.stalkingFocusRange = 10
        self.taskMgr.add(self.cameraStalk, "stalk")

    def cameraStalk(self, task):
        if self.cameraStalkee != None:
            if self.cameraStalkee.model.getPos()[0] - self.camera.getPos()[0] > self.stalkingFocusRange:
                self.camera.setPos(self.cameraStalkee.model.getPos()[0] - self.stalkingFocusRange, 11, -self.cameraZoom)
            elif self.cameraStalkee.model.getPos()[0] - self.camera.getPos()[0] < -self.stalkingFocusRange:
                self.camera.setPos(self.cameraStalkee.model.getPos()[0] + self.stalkingFocusRange, 11, -self.cameraZoom)


        return task.cont

    def initCamera(self):
        self.camera.setPos(0, self.cameraZoom, 11)
