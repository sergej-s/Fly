# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ui_ui as ui
from assets import assets
from fly import *
from fly_qstates import *
from fly_controllers import *
from fly_renders import *
from world import *


class FlyApp(QMainWindow, ui.Ui_FlyApp):
    def __init__(self):
        super(FlyApp, self).__init__()
        self.setupUi(self)

        self.Logo_lbl.setPixmap(QPixmap(assets.sprites['logo']))

        self.game_gb.hide()
        self.gameField_w.setFixedHeight(500)
        self.gameField_w.setFixedWidth(500)
        self.statScroll_scrl.setFixedHeight(500)
        self.stat_text.setStyleSheet("font-size: 14px")
        self.setStyleSheet("QWidget { font-size: 22px}")

        self.startGame_btn.clicked.connect(self.startGame)
        self.stopGame_btn.clicked.connect(self.pauseGame)
        self.addFly_btn.clicked.connect(self.addFly)
        self.newGame_btn.clicked.connect(self.newGame)

    def startGame(self):
        self.game_gb.show()
        self.Logo_lbl.hide()
        self.gameSetting_gb.hide()

        #Game speed is parameter that increase game frame rate relatively of default frame rate
        #GameFrameTime is used in timer to simulate game loop
        self.gameSpeed = self.gameSpeed_sb.value()
        self.gameDefaultFrameRate = 24
        self.gameFrameRate = 6 * self.gameSpeed
        self.gameFrameTime = math.floor(1000/self.gameFrameRate)

        world_cell_count = self.gameFieldCellCount_sb.value()
        world_cell_capacity = self.gameFieldCellCapacity_sb.value()
        self.world = World(self.gameField_w,
                           world_cell_count,
                           world_cell_count,
                           math.floor(self.gameField_w.width()/world_cell_count),
                           math.floor(self.gameField_w.height()/world_cell_count),
                           world_cell_capacity)

        self.flies = []
        self.icons = []
        self.timers = []
        self.stateMachines = []

        #Timer for statistics updating
        timer = QTimer(self)
        self.connect(timer, SIGNAL('timeout()'), self, SLOT('updateStats()'))
        timer.start(1000)
        self.timers.append(timer)


    def pauseGame(self):
        self.updateStats()
        self.stopGame_btn.setText('Продолжить')
        self.stopGame_btn.clicked.connect(self.resumeGame)
        for timer in self.timers:
            timer.stop()

    def resumeGame(self):
        self.stopGame_btn.setText('Остановить')
        self.stopGame_btn.clicked.connect(self.pauseGame)
        for timer in self.timers:
            timer.start()

    def newGame(self):
        self.Logo_lbl.show()
        self.game_gb.hide()
        self.gameSetting_gb.show()
        self.world.clearGrid()
        self.world = None
        for icon in self.icons:
            icon.setParent(None)
        for timer in self.timers:
            timer.deleteLater()
        for machine in self.stateMachines:
            machine.stop()
        self.flies = []
        self.icons = []
        self.timers = []
        self.stateMachines = []


    def addFly(self):
        #There is possibility that fly will not be created due to lack of available cells
        fly = self.createFly()
        if fly:
            #If fly created it is connected with timer which play game loop role.
            self.flies.append(fly)
            timer = QTimer(self)
            self.connect(timer, SIGNAL('timeout()'), fly, SLOT('update()'))
            #Game frame rate is set to this timer
            timer.start(self.gameFrameTime)
            self.timers.append(timer)

    def getDurationInFrames(self, time):
        return math.floor(time/self.gameDefaultFrameRate)

    def createFly(self):

        #Get available cell
        [cell_row, cell_col, cell] = self.world.getRandomAvailibleCell()

        if not cell:
            self.addFly_btn.setEnabled(False)
            return 0

        #QLabel is used as fly animation holder
        icon = QLabel(self.gameField_w)
        icon.setFixedWidth(32)
        icon.setFixedHeight(32)
        icon.show()
        self.icons.append(icon)

        #Fly config parameters
        fly_walking_duration = (self.getDurationInFrames(self.flyWalkingDurationMin_sb.value()),
                                self.getDurationInFrames(self.flyWalkingDurationMax_sb.value()))
        fly_standing_duration = (self.getDurationInFrames(self.flyStandingDurationMin_sb.value()),
                                 self.getDurationInFrames(self.flyStandingDurationMax_sb.value()))
        fly_stupidity = (self.getDurationInFrames(self.flyStupidityMin_sb.value()),
                         self.getDurationInFrames(self.flyStupidityMax_sb.value()))
        fly_life_coef = self.flyLifeCoefficient_sb.value()
        fly_config = dict(width=icon.width(),
                          height=icon.height(),
                          speed=self.flySpeed_sb.value(),
                          stupidity=fly_stupidity,
                          life=(fly_stupidity[0]*fly_life_coef,
                                fly_stupidity[1]*fly_life_coef))

        #Controllers for each fly state
        standing_controller = StandingController(fly_standing_duration)
        walking_controller = WalkingController(fly_walking_duration)
        flying_controller = FlyingController()
        dead_controller = DeadController()

        def get_sprites(sprites, group):
            sprites = [s for (n, s) in sprites.iteritems() if group in n]
            sprites.sort()
            return sprites

        #Renders for each fly state. Renders are connected to animation assets
        walking_render = WalkingRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'walking'))
        standing_render = StandingRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'standing'))
        flying_render = FlyingRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'flying'))
        dead_render = DeadRender(icon, assets.maxFrame, get_sprites(assets.sprites, 'dead'))

        #Create fly with above collected parameters
        fly = Fly(len(self.flies),
                  standing_render,
                  standing_controller,
                  self.world,
                  cell_row,
                  cell_col,
                  fly_config)

        #Put fly to cell and move to random point on it
        cell.addFly(fly)
        [x, y] = cell.getRandomPoint([fly.width, fly.height])
        fly.move(x, y)

        #Add number to fly icon to distinguish one fly from another
        icon_id = QLabel(icon)
        icon_id.setStyleSheet("QLabel { font-size: 8px; color: black}")
        icon_id.setText(str(fly.id))
        icon_id.show()
        self.icons.append(icon_id)

        #Create fly states and connect with controllers and renders
        flying_state = FlyState('flying_state', fly, flying_render, flying_controller)
        walking_state = FlyState('walking_state', fly, walking_render, walking_controller)
        standing_state = FlyState('standing_state', fly, standing_render, standing_controller)
        dead_state = FlyState('dead_state', fly, dead_render, dead_controller)

        #Set transition rules for state changing
        flying_state.addTransition(flying_controller, SIGNAL('standing()'), standing_state)
        walking_state.addTransition(walking_controller, SIGNAL('standing()'), standing_state)
        walking_state.addTransition(walking_controller, SIGNAL('dead()'), dead_state)
        standing_state.addTransition(standing_controller, SIGNAL('walking()'), walking_state)
        standing_state.addTransition(standing_controller, SIGNAL('flying()'), flying_state)
        standing_state.addTransition(standing_controller, SIGNAL('dead()'), dead_state)

        #Initialize Qt State Machine
        machine = QStateMachine(self)
        machine.addState(flying_state)
        machine.addState(walking_state)
        machine.addState(standing_state)
        machine.addState(dead_state)
        machine.setInitialState(standing_state)
        machine.start()
        self.stateMachines.append(machine)

        #Hack to make statistics text field be bigger than text put in it
        self.stat_text.setMinimumHeight(self.stat_text.height() + 80)

        return fly

    @pyqtSlot()
    def updateStats(self):
        stat = 'Общее кол-во мух: ' + str(len(self.flies)) + '\n' \
               + 'пробег измеряется в пикселях' + '\n' \
               + 'возраст в мс' + '\n' \
               + 'скорость в пиксель/мс' + '\n' \
               + '------------------------------' + '\n'
        for fly in self.flies:
            fly_life = fly.life * self.gameFrameTime
            if fly_life > 0:
                fly_speed = fly.mileage / fly_life
            else:
                fly_speed = 0
            stat += 'муха №' + str(fly.id) + ':' + '\n' \
                   + '    пробег ' + str(int(fly.mileage)) + '\n' \
                   + '    возраст ' + str(int(fly_life)) + '/' + str(int(fly.lifetime * self.gameFrameTime)) + '\n' \
                   + '    скорость ' + "{:5.2f}".format(fly_speed) + '\n'
        self.stat_text.setText(stat)


if __name__ == '__main__':
    app = QApplication([])
    w = FlyApp()
    w.show()
    app.exec_()
