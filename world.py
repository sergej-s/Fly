from PySide.QtCore import *


class Cell(QObject):
    def __init__(self, x, y):
        super(Cell, self).__init__()

        self.width = 10
        self.height = 10
        self.x = x
        self.y = y
        self.flyCapacity = 10
        self.flies = []

    def addFly(self, fly):
        self.flies.append(fly)

    def removeFly(self, fly):
        self.flies.remove(fly)

    def isAvalible(self):
        return len(self.flies) < self.flyCapacity


#world = [[Cell(10*n, 10*m) for n in range(0, 100)] for m in range(0, 100)]
world = [[Cell(0, 0)]]
