from PyQt4.QtCore import *
import random
random.seed()

class Fly(QObject):
    def __init__(self,
                 id,
                 fly_render,
                 fly_controller,
                 world,
                 cell_row,
                 cell_col,
                 config):
        super(Fly, self).__init__()
        self.id = id
        self.render = fly_render
        self.controller = fly_controller
        self.world = world
        self.cellRow = cell_row
        self.cellCol = cell_col
        self.width = config['width']
        self.height = config['height']
        self.x = 0
        self.y = 0
        self.mileage = 0
        self.speed = config['speed']
        self.maxStupidity = random.randint(config['stupidity'][0], config['stupidity'][1])
        self.stupidity = self.maxStupidity
        self.lifetime = random.randint(config['life'][0], config['life'][1])
        self.life = 0
        self.direction = [0, 1]

    def __del__(self):
        print 'fly del'
        self.render = None
        self.controller = None
        self.world = None

    def isDead(self):
        return self.life >= self.lifetime

    def isSlowpoke(self):
        return self.stupidity > 0

    def goSlowpoke(self):
        self.stupidity = self.maxStupidity

    @pyqtSlot()
    def update(self):
        #print self.life
        if not self.isDead():
            self.stupidity -= 1
            self.life += 1
        self.controller.update(self, self.world)
        self.render.update(self, self.world)

    def move(self, x, y):
        self.x = x
        self.y = y