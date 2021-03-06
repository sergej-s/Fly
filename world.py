from PyQt4.QtCore import *
from PyQt4.QtGui import *
import random

class Cell(QObject):
    def __init__(self,
                 icon,
                 x,
                 y,
                 width,
                 height,
                 capacity):
        super(Cell, self).__init__()

        self.icon = icon
        self.icon.setFixedWidth(width)
        self.icon.setFixedHeight(height)
        self.icon.setStyleSheet("QLabel { background-color: LightGray; border: 1px solid black; font-size: 10px; color: gray}")
        self.icon.setAlignment(Qt.AlignBottom)
        self.icon.move(x, y)
        self.icon.show()
        self.maxCapacity = capacity
        self.flies = []
        self.setText()

    #def __del__(self):
    #    self.icon.setParent(None)

    def setText(self):
        self.icon.setText(str(self.capacity()) + '/' + str(self.maxCapacity))

    def addFly(self, fly):
        self.flies.append(fly)
        self.setText()

    def removeFly(self, fly):
        self.flies.remove(fly)
        self.setText()

    def isAvalible(self):
        return len(self.flies) < self.maxCapacity

    def capacity(self):
        return len(self.flies)

    def getX(self):
        return self.icon.x()

    def getY(self):
        return self.icon.y()

    def getWidth(self):
        return self.icon.width()

    def getHeight(self):
        return self.icon.height()

    def getRandomPoint(self, offset):
        return [self.getX() + random.randint(0, self.getWidth()-offset[0]),
                self.getY() + random.randint(0, self.getHeight()-offset[1])]


class World(QObject):
    def __init__(self,
                 cell_widget,
                 cell_row_count,
                 cell_col_count,
                 cell_width,
                 cell_height,
                 capacity):
        super(World, self).__init__()
        self.rowCount = cell_row_count
        self.colCount = cell_col_count
        self.grid = [[Cell(QLabel(cell_widget), n*cell_width, m*cell_height, cell_width, cell_height, capacity)
                     for n in range(0, cell_col_count)]
                     for m in range(0, cell_row_count)]

    def getCell(self, row, col):
        if row >= 0 and row < len(self.grid) and col >= 0 and col < len(self.grid[row]):
            return self.grid[row][col]
        else:
            return 0

    def getRandomAvailibleCell(self):
        available_cells = []
        for row_ind, cells in enumerate(self.grid):
            for col_ind, cell in enumerate(cells):
                if cell.isAvalible():
                    available_cells.append([row_ind, col_ind, cell])
        if len(available_cells) > 0:
            cell = available_cells[random.randint(0, len(available_cells) - 1)]
            return cell
        else:
            return [-1, -1, None]

    #def __del__(self):
    #    self.clearGrid()

    def clearGrid(self):
        map(lambda cell: cell.icon.setParent(None), sum(self.grid, []))

