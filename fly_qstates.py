from PySide.QtCore import *


class FlyState(QState):
    def __init__(self, name, fly, fly_render, fly_controller):
        super(FlyState, self).__init__()
        self.name = name
        self.fly = fly
        self.flyRender = fly_render
        self.flyController = fly_controller

    def onEntry(self, e):
        #print(self.name + ' state enter')
        self.fly.controller = self.flyController
        self.fly.render = self.flyRender
        self.fly.update()

    def onExit(self, e):
        self.fly.controller.reset()
        self.fly.render.reset()
