from PyQt4.QtCore import *
import math
import random
random.seed()

def getVectorLength(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2)


def getNormalizedVector(vector):
    length = getVectorLength(vector)
    vector_norm = [vector[0]/length, vector[1]/length]
    return vector_norm


class FlyController(QObject):
    flying = pyqtSignal()
    standing = pyqtSignal()
    walking = pyqtSignal()
    dead = pyqtSignal()

    def __init__(self, state_duration=(50, 100)):
        super(FlyController, self).__init__()

        self._stateMinDuration = state_duration[0]
        self._stateMaxDuration = state_duration[1]
        self._stateDuration = self._stateMaxDuration
        self._started = True

    def reset(self):
        self._stateDuration = random.randint(self._stateMinDuration, self._stateMaxDuration)
        self._started = True

    def _isFinished(self):
        return self._stateDuration <= 0

    def update(self, fly, world):
        self._stateDuration -= 1

    def _directFly(self, fly, world):
        cell = world.grid[fly.cellRow][fly.cellCol]
        [x, y] = cell.getRandomPoint([fly.width, fly.height])
        x = x - fly.x
        y = y - fly.y
        vector = getNormalizedVector([x, y])
        self._maxPathLength = getVectorLength([x, y])
        self._origin = [fly.x, fly.y]
        self._direction = vector
        fly.direction = vector

    def _moveFly(self, fly, world):
        x = fly.x + self._direction[0] * fly.speed
        y = fly.y + self._direction[1] * fly.speed

        path_length = getVectorLength([x - self._origin[0], y - self._origin[1]])

        if path_length >= self._maxPathLength:
            self._direction = 0
            return 0 #fly stopped
        else:
            fly.x = x
            fly.y = y
            fly.mileage += path_length
            return 1 #fly moved


class FlyingController(FlyController):
    def __init__(self):
        super(FlyingController, self).__init__()
        self._direction = 0

    def update(self, fly, world):
        super(FlyingController, self).update(fly, world)
        if self._started:
            self._started = False
            self._direction = 0

        if not self._direction:
            self._directFly(fly, world)

        if not self._moveFly(fly, world):
            fly.goSlowpoke()
            self.standing.emit()
            return


class WalkingController(FlyController):
    def __init__(self, state_duration):
        super(WalkingController, self).__init__(state_duration)
        self._direction = 0

    def update(self, fly, world):
        super(WalkingController, self).update(fly, world)

        if self._started:
            self._started = False
            self._direction = 0

        if fly.isDead():
            self.dead.emit()
            return

        if (not fly.isSlowpoke()) or self._isFinished():
            self.standing.emit()
            return

        if not self._direction:
            self._directFly(fly, world)

        self._moveFly(fly, world)


class StandingController(FlyController):
    def __init__(self, state_duration):
        super(StandingController, self).__init__(state_duration)

    def update(self, fly, world):
        super(StandingController, self).update(fly, world)
        if self._started:
            self._started = False
            self._direction = 0

        if fly.isDead():
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

        if self._isFinished():
            self.walking.emit()


class DeadController(FlyController):
    def __init__(self):
        super(DeadController, self).__init__()

    def update(self, fly, world):
        pass
