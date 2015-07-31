from PyQt4.QtGui import *
from PyQt4.QtCore import *
from assets import assets
import math
import random
import ui_ui as ui
from fly import *
from fly_qstates import *
from fly_controllers import *
from fly_renders import *
from world import *


class FlyApp(QMainWindow, ui.Ui_FlyApp):
    def __init__(self):
        super(FlyApp, self).__init__()
        self.setupUi(self)

        self.gameField_w.hide()
        self.stopGame_btn.hide()
        self.addFly_btn.hide()
        self.gameField_w.setFixedHeight(500)
        self.gameField_w.setFixedWidth(500)
        #self.gameField_w.setStyleSheet("QWidget { border: 1px solid black; font-size: 10px}")

        self.startGame_btn.clicked.connect(self.startGame)
        self.stopGame_btn.clicked.connect(self.stopGame)
        self.addFly_btn.clicked.connect(self.addFly)

    def startGame(self):
        self.gameField_w.show()
        self.stopGame_btn.show()
        self.addFly_btn.show()
        self.gameSetting_gb.hide()
        self.startGame_btn.hide()

        self.game_speed = math.floor(1000/self.gameSpeed_sb.value())

        world_cell_count = self.gameFieldCellCount_sb.value()
        world_cell_capacity = self.gameFieldCellCapacity_sb.value()
        self.world = World(self.gameField_w,
                           world_cell_count,
                           world_cell_count,
                           math.floor(self.gameField_w.width()/world_cell_count),
                           math.floor(self.gameField_w.height()/world_cell_count),
                           world_cell_capacity)

        self.flies = []

    def stopGame(self):
        self.gameField_w.hide()
        self.stopGame_btn.hide()
        self.addFly_btn.hide()
        self.gameSetting_gb.show()
        self.startGame_btn.show()

    def addFly(self):
        fly = self.createFly()
        self.flies.append(fly)
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), fly, SLOT('update()'))
        timer.start(self.game_speed)

    def createFly(self):
        icon = QLabel(self.gameField_w)
        icon.setFixedWidth(32)
        icon.setFixedHeight(32)
        icon.show()

        fly_walking_duration = (self.flyWalkingDurationMin_sb.value(), self.flyWalkingDurationMax_sb.value())
        fly_standing_duration = (self.flyStandingDurationMin_sb.value(), self.flyStandingDurationMax_sb.value())
        fly_stupidity = (self.flyStupidityMin_sb.value(), self.flyStupidityMax_sb.value())
        fly_life_coef = self.flyLifeCoefficient_sb.value()
        fly_config = dict(width=icon.width(),
                          height=icon.height(),
                          speed=self.flySpeed_sb.value(),
                          stupidity=fly_stupidity,
                          life=(fly_stupidity[0]*fly_life_coef,
                                fly_stupidity[1]*fly_life_coef))

        standing_controller = StandingController(icon, fly_standing_duration)
        walking_controller = WalkingController(icon, fly_walking_duration)
        flying_controller = FlyingController(icon)
        dead_controller = DeadController(icon)

        def get_sprites(sprites, group):
            sprites = [s for (n, s) in sprites.iteritems() if group in n]
            sprites.sort()
            return sprites

        walking_render = WalkingRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'walking'))
        standing_render = StandingRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'standing'))
        flying_render = FlyingRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'flying'))
        dead_render = DeadRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'dead'))

        fly = Fly(standing_render,
                  standing_controller,
                  self.world,
                  random.randint(0, self.world.rowCount - 1),
                  random.randint(0, self.world.colCount - 1),
                  fly_config)

        flying_state = FlyState('flying_state', fly, flying_render, flying_controller)
        walking_state = FlyState('walking_state', fly, walking_render, walking_controller)
        standing_state = FlyState('standing_state', fly, standing_render, standing_controller)
        dead_state = FlyState('dead_state', fly, dead_render, dead_controller)

        flying_state.addTransition(flying_controller, SIGNAL('standing()'), standing_state)
        walking_state.addTransition(walking_controller, SIGNAL('standing()'), standing_state)
        walking_state.addTransition(walking_controller, SIGNAL('dead()'), dead_state)
        standing_state.addTransition(standing_controller, SIGNAL('walking()'), walking_state)
        standing_state.addTransition(standing_controller, SIGNAL('flying()'), flying_state)
        standing_state.addTransition(standing_controller, SIGNAL('dead()'), dead_state)

        machine = QStateMachine(self)
        machine.addState(flying_state)
        machine.addState(walking_state)
        machine.addState(standing_state)
        machine.addState(dead_state)
        machine.setInitialState(standing_state)
        machine.start()

        return fly

if __name__ == '__main__':
    app = QApplication([])
    w = FlyApp()
    w.show()
    app.exec_()
