from PySide.QtCore import *


class Fly(QObject):
    def __init__(self, fly_render, fly_controller, world, cell_ind):
        super(Fly, self).__init__()
        self.render = fly_render
        self.controller = fly_controller
        self.world = world
        self.cellInd = cell_ind
        self.x = 0
        self.y = 0

    def update(self):
        self.controller.start(self, self.world)
        self.render.start(self, self.world)