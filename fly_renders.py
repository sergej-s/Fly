from PySide.QtCore import *
from PySide.QtGui import *


class FlyRender(QObject):
    def __init__(self, icon, sprites):
        super(FlyRender, self).__init__()
        self.icon = icon
        self.animationSpeed = 40
        self.currentFrame = 0
        self.currentAngle = 0

        self.sprites = []
        for sprite in sprites:
            self.sprites.append(QPixmap(sprite))

    def changeFrame(self):
        if self.currentFrame == 3:
            self.currentFrame = 0
        else:
            self.currentFrame += 1

    def animate(self):
        self.icon.setPixmap(self.sprites[self.currentFrame])
        self.changeFrame()

    def stop(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.currentFrame = 0

    def start(self, fly, world):
        print('render update')
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'), self, SLOT('animate()'))
        self.timer.start(self.animationSpeed)


class FlyingRender(FlyRender):
    def __init__(self, icon, sprites):
        super(FlyingRender, self).__init__(icon, sprites)
        self.icon.setStyleSheet("Qicon { background-color: gray }")
        self.icon.setPixmap(self.sprites[0])


class SlowpokeRender(FlyRender):
    def __init__(self, icon, walking_sprites, standing_sprites):
        self.sprites = walking_sprites + standing_sprites
        super(SlowpokeRender, self).__init__(icon, self.sprites)
        self.walkingSprites = walking_sprites
        self.standingSprites = standing_sprites
        self.icon.setStyleSheet("Qicon { background-color: gray }")
        self.icon.setPixmap(self.walkingSprites[0])
        self.animationSpeed = 40
        print(self.walkingSprites)

    def animate(self):
        #print(self.walkingSprites[self.currentFrame])
        self.icon.setPixmap(self.walkingSprites[self.currentFrame])
        self.changeFrame()

    def start(self, fly, world):
        print('slowpoke render update')
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'), self, SLOT('animate()'))
        self.timer.start(self.animationSpeed)


class DeadRender(FlyRender):
    def __init__(self, parent, sprites):
        super(DeadRender, self).__init__(parent, sprites)
        self.icon.setStyleSheet("Qicon { background-color: gray }")
        self.icon.setPixmap(self.sprites[0])
        self.animationSpeed = 40

    def start(self, fly, world):
        print('dead render update')
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL('timeout()'), self, SLOT('animate()'))
        self.timer.start(self.animationSpeed)
