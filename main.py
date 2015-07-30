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


class flyApp(QMainWindow, ui.Ui_FlyApp):
    def __init__(self):
        super(flyApp, self).__init__()
        self.setupUi(self)

        icon = QLabel(self.gameField_w)

        slowpoke_controller = SlowpokeController(icon)
        flying_controller = FlyingController(icon)
        dead_controller = DeadController(icon)

        def getSprites(sprites, group):
            sprites = [s for (n, s) in assets.sprites.iteritems() if group in n]
            sprites.sort()
            return sprites

        slowpoke_render = SlowpokeRender(icon,
                                         getSprites(assets.sprites, 'walking'),
                                         getSprites(assets.sprites, 'standing'))
        flying_render = FlyingRender(icon, getSprites(assets.sprites, 'flying'))
        dead_render = DeadRender(icon, getSprites(assets.sprites, 'dead'))

        fly = Fly(slowpoke_render, slowpoke_controller, world, 0)

        flying_state = FlyState('flying_state', fly, flying_render, flying_controller)
        slowpoke_state = FlyState('slowpoke_state', fly, slowpoke_render, slowpoke_controller)
        dead_state = FlyState('dead_state', fly, dead_render, dead_controller)

        flying_state.addTransition(flying_controller, SIGNAL('standing()'), slowpoke_state)
        slowpoke_state.addTransition(slowpoke_controller, SIGNAL('flying()'), flying_state)
        slowpoke_state.addTransition(slowpoke_controller, SIGNAL('dead()'), dead_state)

        machine = QStateMachine(self)
        machine.addState(flying_state)
        machine.addState(slowpoke_state)
        machine.addState(dead_state)
        machine.setInitialState(slowpoke_state)
        machine.start()


if __name__ == '__main__':
    app = QApplication([])
    w = flyApp()
    w.show()
    app.exec_()
