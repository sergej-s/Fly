from PySide.QtCore import *
import math
import random


def getVectorLength(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)


def getNormalizedVector(vector):
    length = getVectorLength(vector)
    vector_norm = [vector[0]/length, vector[1]/length]
    return vector_norm


class FlyController(QObject):
    flying = Signal()
    standing = Signal()
    walking = Signal()
    dead = Signal()

    def __init__(self, icon, state_duration=(50, 100)):
        super(FlyController, self).__init__()
        self.icon = icon

        self.stateMaxDuration = state_duration[1]
        self.stateMinDuration = state_duration[0]
        self.stateDuration = self.stateMaxDuration
        self.started = 1

    def reset(self):
        self.stateDuration = random.randint(self.stateMinDuration, self.stateMaxDuration)
        self.started = 1

    def isFinished(self):
        return self.stateDuration <= 0

    def update(self, fly, world):
        self.stateDuration -= 1

    def directFly(self, fly, world):
        cell = world.grid[fly.cellRow][fly.cellCol]
        [x, y] = cell.getRandomPoint([fly.width, fly.height])
        x = x - fly.x
        y = y - fly.y
        vector = getNormalizedVector([x, y])
        self.maxPathLength = getVectorLength([x, y])
        self.origin = [fly.x, fly.y]
        self.direction = vector
        fly.direction = vector

    def moveFly(self, fly, world):
        x = fly.x + self.direction[0] * fly.speed
        y = fly.y + self.direction[1] * fly.speed

        path_length = getVectorLength([x - self.origin[0], y - self.origin[1]])

        if path_length >= self.maxPathLength:
            self.direction = 0
            return 0 #fly stopped
        else:
            fly.x = x
            fly.y = y
            return 1 #fly moved


class FlyingController(FlyController):
    def __init__(self, icon):
        super(FlyingController, self).__init__(icon)
        self.direction = 0

    def update(self, fly, world):
        super(FlyingController, self).update(fly, world)
        if self.started:
            self.started = 0
            self.direction = 0

        if not self.direction:
            self.directFly(fly, world)

        if not self.moveFly(fly, world):
            fly.goSlowpoke()
            self.standing.emit()
            return


class WalkingController(FlyController):
    def __init__(self, icon, state_duration):
        super(WalkingController, self).__init__(icon, state_duration)
        self.direction = 0

    def update(self, fly, world):
        super(WalkingController, self).update(fly, world)

        if self.started:
            self.started = 0
            self.direction = 0

        if fly.life <= 0:
            self.dead.emit()
            return

        if not fly.isSlowpoke() or self.isFinished():
            self.standing.emit()
            return

        if not self.direction:
            self.directFly(fly, world)

        self.moveFly(fly, world)


class StandingController(FlyController):
    def __init__(self, icon, state_duration):
        super(StandingController, self).__init__(icon, state_duration)

    def update(self, fly, world):
        super(StandingController, self).update(fly, world)
        if self.started:
            self.started = 0
            self.direction = 0

        if fly.life <= 0:
            self.dead.emit()
            return

        if not fly.isSlowpoke():
            cell_neighbor_ind = random.randint(0, 3) #0 - top, 1 - right, 2 - bottom, 3 - left
            next_cell_row = -1
            next_cell_col = -1
            if cell_neighbor_ind == 0:
                next_cell_row = fly.cellRow
                next_cell_col = fly.cellCol + 1
            elif cell_neighbor_ind == 1:
                next_cell_row = fly.cellRow + 1
                next_cell_col = fly.cellCol
            elif cell_neighbor_ind == 2:
                next_cell_row = fly.cellRow
                next_cell_col = fly.cellCol - 1
            elif cell_neighbor_ind == 3:
                next_cell_row = fly.cellRow - 1
                next_cell_col = fly.cellCol

            next_cell = world.getCell(next_cell_row, next_cell_col)
            if next_cell and next_cell.isAvalible():
                current_cell = world.getCell(fly.cellRow, fly.cellCol)
                current_cell.removeFly(fly)
                fly.cellRow = next_cell_row
                fly.cellCol = next_cell_col
                next_cell.addFly(fly)
                self.flying.emit()
                return
            else:
                fly.goSlowpoke()

        if self.isFinished():
            self.walking.emit()


class DeadController(FlyController):
    def __init__(self, icon):
        super(DeadController, self).__init__(icon)

    def update(self, fly, world):
        pass
