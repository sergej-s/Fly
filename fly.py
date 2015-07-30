from PySide.QtCore import *
import random

class Fly(QObject):
    def __init__(self,
                 fly_render,
                 fly_controller,
                 world,
                 cell_row,
                 cell_col,
                 config):
        super(Fly, self).__init__()
        self.render = fly_render
        self.controller = fly_controller
        self.world = world
        self.cellRow = cell_row
        self.cellCol = cell_col
        self.width = config['width']
        self.height = config['height']
        cell = world.getCell(cell_row, cell_col)
        cell.addFly(self)
        [self.x, self.y] = cell.getRandomPoint([self.width, self.height])
        self.speed = config['speed']
        self.maxStupidity = random.randint(config['stupidity'][0], config['stupidity'][1])
        self.stupidity = self.maxStupidity
        self.life = random.randint(config['life'][0], config['life'][1])
        self.direction = [0, 1]

    def isSlowpoke(self):
        return self.stupidity > 0

    def goSlowpoke(self):
        self.stupidity = self.maxStupidity

    def update(self):
        #print('life', self.life)
        self.stupidity -= 1
        self.life -= 1
        self.controller.update(self, self.world)
        self.render.update(self, self.world)

    def move(self, x, y):
        self.x = x
        self.y = y