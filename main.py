from PySide.QtGui import *
from PySide.QtCore import *
from assets import assets
import math
import random
import ui_uis as ui
from fly import *
from fly_qstates import *
from fly_controllers import *
from fly_renders import *
from world import *


class FlyApp(QMainWindow, ui.Ui_FlyApp):
    def __init__(self):
        super(FlyApp, self).__init__()
        self.setupUi(self)

        self.world = World(self.gameField_w, 5, 5, 100, 100, 4)

        self.flies = []
        for i in range(20):
            fly = self.createFly()
            self.flies.append(fly)
            timer = QTimer(self)
            self.connect(timer, SIGNAL('timeout()'), fly, SLOT('update()'))
            timer.start(40)


    def createFly(self):
        icon = QLabel(self.gameField_w)
        icon.setFixedWidth(32)
        icon.setFixedHeight(32)

        standing_controller = StandingController(icon, (20, 50))
        walking_controller = WalkingController(icon, (20, 50))
        flying_controller = FlyingController(icon)
        dead_controller = DeadController(icon)

        def get_sprites(sprites, group):
            sprites = [s for (n, s) in assets.sprites.iteritems() if group in n]
            sprites.sort()
            return sprites

        max_frame = 3

        walking_render = WalkingRender(icon, max_frame, get_sprites(assets.sprites, 'walking'))
        standing_render = StandingRender(icon, max_frame, get_sprites(assets.sprites, 'standing'))
        flying_render = FlyingRender(icon, max_frame, get_sprites(assets.sprites, 'flying'))
        dead_render = DeadRender(icon, max_frame, get_sprites(assets.sprites, 'dead'))

        fly_config = dict(width=32,
                          height=32,
                          speed=3,
                          stupidity=[50, 200],
                          life=[500, 1000])

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
