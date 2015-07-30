from PySide.QtCore import *


class FlyController(QObject):
    flying = Signal()
    standing = Signal()
    dead = Signal()

    def __init__(self, icon):
        super(FlyController, self).__init__()
        self.icon = icon

        self.icon.mousePressEvent = self.mouseDown
        self.icon.mouseMoveEvent = self.mouseMove

    def stop(self):
        pass

    def start(self, fly, world):
        pass

    def mouseDown(self, event):
        self.oldPos = event.globalPos()

    def mouseMove(self, event):
        delta = event.globalPos() - self.oldPos
        self.icon.move(self.icon.x() + delta.x(), self.icon.y() + delta.y())
        self.oldPos = event.globalPos()


class FlyingController(FlyController):
    def __init__(self, icon):
        super(FlyingController, self).__init__(icon)

    def finish(self):
        self.standing.emit()
        print(123)

    def start(self, fly, world):
        timer = QTimer(self)
        timer.setSingleShot(True)
        self.connect(timer, SIGNAL('timeout()'), self, SLOT('finish()'))
        timer.start(3000)


class SlowpokeController(FlyController):
    def __init__(self, icon):
        super(SlowpokeController, self).__init__(icon)

    def finish(self):
        self.dead.emit()
        print(321)

    def start(self, fly, world):
        timer = QTimer(self)
        timer.setSingleShot(True)
        self.connect(timer, SIGNAL('timeout()'), self, SLOT('finish()'))
        timer.start(3000)



class DeadController(FlyController):
    def __init__(self, icon):
        super(DeadController, self).__init__(icon)

    def start(self, fly, world):
        pass
