from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math

class FlyRender(QObject):
    def __init__(self, icon, max_frame, sprites):
        super(FlyRender, self).__init__()
        self.icon = icon
        self.currentFrame = 0
        self.maxFrame = max_frame
        self.sprites = []
        for sprite in sprites:
            self.sprites.append(QPixmap(sprite))
        self.icon.setPixmap(self.sprites[0])
        self.frame_offset = 0

    def changeFrame(self):
        if self.currentFrame == self.maxFrame:
            self.currentFrame = 0
        else:
            self.currentFrame += 1

    def reset(self):
        pass

    def update(self, fly, world):
        self.icon.move(fly.x, fly.y)
        #transform = QTransform()
        #transform = transform.scale(math.sqrt(sprite.size().width()), math.sqrt(sprite.size().height()))
        # print(fly.direction[1])
        # angle = math.degrees(math.acos(fly.direction[1]))
        # if fly.direction[1] < 0:
        #     angle = 360 - angle
        # print(angle)
        # transform = transform.rotate(angle)
        # self.icon.setPixmap(self.sprites[self.currentFrame].transformed(transform))
        self.icon.setPixmap(self.sprites[self.currentFrame + self.frame_offset])
        self.changeFrame()


class FlyingRender(FlyRender):
    def __init__(self, icon, max_frame, sprites):
        super(FlyingRender, self).__init__(icon, max_frame, sprites)


class WalkingRender(FlyRender):
    def __init__(self, icon, max_frame, sprites):
        super(WalkingRender, self).__init__(icon, max_frame, sprites)

    def update(self, fly, world):
        if fly.stupidity > 0.66 * fly.maxStupidity:
            self.frame_offset = 8
        elif fly.stupidity < 0.33 * fly.maxStupidity:
            self.frame_offset = 0
        else:
            self.frame_offset = 4
        super(WalkingRender, self).update(fly, world)


class StandingRender(FlyRender):
    def __init__(self, icon, max_frame, sprites):
        super(StandingRender, self).__init__(icon, max_frame, sprites)

    def update(self, fly, world):
        if fly.stupidity > 0.66 * fly.maxStupidity:
            self.frame_offset = 8
        elif fly.stupidity < 0.33 * fly.maxStupidity:
            self.frame_offset = 0
        else:
            self.frame_offset = 4
        super(StandingRender, self).update(fly, world)


class DeadRender(FlyRender):
    def __init__(self, parent, max_frame, sprites):
        super(DeadRender, self).__init__(parent, max_frame, sprites)

    def update(self, fly, world):
        if self.currentFrame != self.maxFrame:
            super(DeadRender, self).update(fly, world)
