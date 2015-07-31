from PyQt4.QtCore import *

#Each fly can be in 4 states:
#1. Standing
#2. Walking
#3. Flying
#4. Dead
#In standing and walking states fly starts to slowpoke until stupidity parameter is reached zero.

class FlyState(QState):
    def __init__(self, name, fly, fly_render, fly_controller):
        super(FlyState, self).__init__()
        self.name = name
        self.fly = fly
        self.flyRender = fly_render
        self.flyController = fly_controller

    def __del__(self):
        self.fly = None
        self.flyRender = None
        self.flyController = None

    #Change controller and render accordingly to current state
    def onEntry(self, e):
        #print(self.name + ' state enter')
        self.fly.controller = self.flyController
        self.fly.render = self.flyRender
        self.fly.update()

    #Reset controller and render on leaving state
    def onExit(self, e):
        self.fly.controller.reset()
        self.fly.render.reset()
